import requests
import os
import time
from threading import Thread
import shutil

list_task_url = "https://scheduler.biocomputingup.it/task/"
list_script_url = "https://scheduler.biocomputingup.it/script/"
list_params_url = "https://scheduler.biocomputingup.it/params/"

class Status:
    statusMap = {
        "task has been rejected from the ws": "failed",
        "task has been received from the ws": "pending",
        "task has been created and sent to the DRM": "pending",
        "process status cannot be determined": "pending",
        "job is queued and active": "running",
        "job is queued and in system hold": "running",
        "job is queued and in user hold": "running",
        "job is queued and in user and system hold": "running",
        "job is running": "running",
        "job is system suspended": "pending",
        "job is user suspended": "pending",
        "job finished normally": "success",
        "job finished, but failed": "failed",
        "job has been deleted": "deleted"
    }

    def __init__(self, status):
        self.status = self.decode_status(status)

    def __repr__(self):
        return self.status

    def __eq__(self, other):
        return self.status == other

    def decode_status(self, status_long):
        return self.statusMap[status_long]


class Task:
    _status: [Status, None] = None
    _uuid: [str, None] = None

    def __init__(self, uuid=None, status=None):
        self.uuid = uuid
        self.status = status

    def __repr__(self) -> str:
        return "{} - {}".format(self.uuid, self.status)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = Status(status) if status is not None else status

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        self._uuid = uuid

    def is_finished(self) -> bool:
        return self._status == "failed" or self._status == "deleted" or self._status == "success"


def check_for_job(task):
    try:
        job_url = "{}/{}".format(list_task_url, task.uuid)

        while not task.is_finished():
            response = requests.get(job_url, timeout=5)
            response.raise_for_status()
            task.status = response.json()["status"]
            if not task.is_finished():
                time.sleep(3)

    except requests.exceptions.RequestException as err:
        return err


def post_job(task, file_pth, params):
    try:
        files = {'input_file': open(file_pth, 'rb')}

        response = requests.post(list_task_url, files=files, data=params, timeout=5)
        response.raise_for_status()
        task.uuid = response.json()["uuid"]
        task.status = response.json()["status"]

    except requests.exceptions.RequestException as err:
        return err


def download_results(task, extract_pth):
    if task.status == "failed":
        return
    try:
        output_url = "{}/{}/{}".format(list_task_url, task.uuid, "download")

        response = requests.get(output_url, timeout=5)
        response.raise_for_status()
        file_name = response.headers["content-disposition"].split("filename=")[1]
        file_pth = "{}/{}".format(extract_pth, file_name)

        with open(file_pth, "wb") as f:
            f.write(response.content)

        shutil.unpack_archive(file_pth, extract_pth)
        os.remove(file_pth)

    except requests.exceptions.RequestException as err:
        return err


def config_to_parameters(config):
    convert = {
        "-g": "seq_sep",
        "-o": "len_salt",
        "-s": "len_ss",
        "-k": "len_pipi",
        "-a": "len_pica",
        "-b": "len_hbond",
        "-w": "len_vdw"
    }

    new_config = {}

    for key, value in config.items():
        if key in convert:
            new_config[convert[key]] = value.strip("--")

    new_config[config["edges"].strip("--")] = True

    return new_config


def run_ring_api(file_pth, run_config, tmp_dir, progress_f):

    task = Task()

    file_name = os.path.basename(file_pth)

    parameters = {
        "task_name": "ring-plugin-api",
        "original_name": file_name
    }

    parameters.update(config_to_parameters(run_config))

    t_post_job = Thread(target=post_job, args=(task, file_pth, parameters))
    t_post_job.start()

    prev_progress = 0
    while t_post_job.is_alive():
        progress_f(min([prev_progress, 15]))
        prev_progress += 0.01

    t_check_job = Thread(target=check_for_job, args=(task,))
    t_check_job.start()

    prev_progress = 15
    timer = time.time() - 5
    while t_check_job.is_alive():
        if time.time() - timer > 5:
            timer = time.time()

        progress_f(min([prev_progress, 85]))
        prev_progress += 0.00001

    t_download_results = Thread(target=download_results, args=(task, tmp_dir))
    t_download_results.start()

    prev_progress = 85

    while t_download_results.is_alive():
        progress_f(min([prev_progress, 100]))
        prev_progress += 0.01

    progress_f(100)