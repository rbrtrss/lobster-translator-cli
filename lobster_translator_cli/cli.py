import cloup
import os

FILE_TYPES = ["car", "list"]
INDEX_TYPES = ["cohp", "cobi", "coop"]

@cloup.command()
@cloup.argument('dir_path', type=cloup.Path(resolve_path=True))
@cloup.option("--subdir / --singledir", "-r / ", default=False)
@cloup.option("--file_type", "-f", type=cloup.Choice(FILE_TYPES))
@cloup.option("--index_type", "-i", type=cloup.Choice(INDEX_TYPES))
def process(dir_path, subdir, file_type, index_type):
    """
    When do we print this?
    """
    # Catch all inputs
    if subdir:
        working_paths = gen_subdirs_arr(dir_path)
    else:
        working_paths = [dir_path]

    if file_type == None:
        files_arr = FILE_TYPES
    else:
        files_arr = [file_type]

    if index_type == None:
        index_arr = INDEX_TYPES
    else:
        index_arr = [index_type]
    # End catch all inputs
    
    print(working_paths)
    
    both = gen_filenames_dict(working_paths, files_arr, index_arr)
    print(both['list'])

def gen_filenames_dict(paths_arr, files_arr, index_arr):
    return { f : [os.path.join(p,build_filename(f,i)) for p in paths_arr for i in index_arr ] for f in files_arr }


def gen_filenames_arr(paths_arr, files_arr, index_arr):
    return [ [ os.path.join(p,build_filename(f,i)) for i in index_arr ] for f in files_arr for p in paths_arr] # inner on filetype

def gen_subdirs_arr(dir_path):
    return [os.path.join(dir_path,d) for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]

def build_filename(file, index):
    filename = (index + file).upper() + ".lobster"
    if file == "list":
        filename = "I" + filename
    return filename