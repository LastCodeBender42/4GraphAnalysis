from pymol import cmd

@cmd.extend
def get_protein_name():
    objects = cmd.get_object_list()
    if objects:
        return objects[0]
    else:
        return None
