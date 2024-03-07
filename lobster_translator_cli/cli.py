import cloup
import os
from .io import carfile_to_df, listfile_to_df
import pandas as pd

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
    full_filepaths = gen_filenames_dict(working_paths, files_arr, index_arr)

    for file in files_arr:
        if file == "car":
            print(lobster_car_to_string(full_filepaths, index_arr))
        elif file == "list":
            print(lobster_list_to_string(full_filepaths, index_arr))
        # else:
        #     raise Exception("Considering a non processable file type")


    # print(full_filepaths['list'])


def gen_filenames_dict(paths_arr, files_arr, index_arr):
    return { f : [create_if_exists(p, f, i) for p in paths_arr for i in index_arr ] for f in files_arr }
    # return { f : [os.path.join(p,build_filename(f,i)) for p in paths_arr for i in index_arr ] for f in files_arr }


def gen_filenames_arr(paths_arr, files_arr, index_arr):
    return [ [ os.path.join(p,build_filename(f,i)) for i in index_arr ] for f in files_arr for p in paths_arr] # inner on filetype

def gen_subdirs_arr(dir_path):
    return [os.path.join(dir_path,d) for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]

def create_if_exists(path, file, index):
    full_filepath = os.path.join(path,build_filename(file,index))
    if not os.path.exists(full_filepath):
        raise FileNotFoundError(f"The {full_filepath} does not exist")
    
    return full_filepath

def build_filename(file, index):
    filename = (index + file).upper() + ".lobster"
    if file == "list":
        filename = "I" + filename
    return filename

def lobster_car_to_string(lobster_dict, index_arr):
    out_arr = []
    car_arr = lobster_dict["car"]
    for i in range(len(car_arr)):
        structure, df = carfile_to_df(car_arr[i])
        out_arr.append(f'# {index_arr[i]} {structure} \n' + df.to_csv(sep=',', index=None))
    
    return '\n\n'.join(out_arr)

def lobster_list_to_string(lobster_dict, index_arr):
    updated_index = [ 'i' + index for index in index_arr ]
    out_dict = { i : [] for i in updated_index }
    # out_dict = {}
    list_arr = lobster_dict["list"]
    for list in list_arr:
        indicator, df = listfile_to_df(list)
        out_dict[indicator].append(df)
        # out_arr.append(index_arr[i])
    
    casi_dict = { k : pd.concat(v) for k,v in out_dict.items()}
    # return "\n\n".join(out_arr)
    return f"{casi_dict["icobi"]}"