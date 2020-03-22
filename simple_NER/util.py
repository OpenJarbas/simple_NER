from os.path import join, dirname, isfile, expanduser, isdir
from os import listdir


def resolve_resource_file(res_name, lang="en-us"):
    """Convert a resource into an absolute filename.

    Resource names are in the form: 'filename.ext'
    or 'path/filename.ext'

    The system wil look for simple_NER/res/res_name first, and
    if not found will look in language subfolders

    Args:
        res_name (str): a resource path/name
    Returns:
        str: path to resource or None if no resource found
    """

    # First look for fully qualified file (e.g. a user setting)
    if isfile(res_name):
        return res_name

    # Next look for /simple_NER/res/res_name
    data_dir = join(dirname(__file__), "res")
    filename = expanduser(join(data_dir, res_name))
    if isfile(filename):
        return filename

    # Next look for /simple_NER/res/{lang}/res_name
    data_dir = join(dirname(__file__), "res", lang)
    filename = expanduser(join(data_dir, res_name))
    if isfile(filename):
        return filename

    # Next look for /simple_NER/res/{lang_short}/res_name
    data_dir = join(dirname(__file__), "res", lang.split("-")[0])
    filename = expanduser(join(data_dir, res_name))
    if isfile(filename):
        return filename

    # Next look for /simple_NER/res/{lang-short}-XX/res_name
    data_dir = join(dirname(__file__), "res")
    for folder in listdir(data_dir):
        if folder.startswith(lang.split("-")[0]):
            filename = expanduser(join(data_dir, folder, res_name))
            if isfile(filename):
                return filename

    return None  # Resource cannot be resolved

