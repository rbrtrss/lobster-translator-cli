# import click
import cloup
from cloup import option, option_group, constraint
from cloup.constraints import mutually_exclusive, RequireExactly
import os

ORIGIN = ['car', 'list']
INDICES = ['cobi', 'cohp', 'coop']

origin_options = option_group(
    'Choose between carfiles or listfiles',
    option('--todo', 'filetype', help='Read all files'),
    option('-c', '--carfile', 'filetype', help='Read carfiles'),
    option('-l', '--listfile', 'filetype', help='Read listfiles'),
    # constraint=RequireExactly(1)
)

index_options = option_group(
    'Available files to process',
    option('--mucho', 'filename', help='Read all indices'),
    option('-b', '--cobi', 'filename', help='Read cobifile'),
    option('-h', '--cohp', 'filename', help='Read cohpfile'),
    option('-o', '--coop', 'filename', help='Read coopfile'),
)

@cloup.command()
@cloup.argument('dir_path', type=cloup.Path(exists=True))
@origin_options
@index_options
# @option_group(
#     'Choose between carfiles or listfiles',
#     option('--todo', 'filetype', flag_value=ORIGIN, help='Read all files'),
#     option('-c', '--carfile', 'filetype', flag_value=[ORIGIN[0]], help='Read carfiles'),
#     option('-l', '--listfile', 'filetype', flag_value=[ORIGIN[1]], help='Read listfiles'),
#     constraint=RequireExactly(1)
# )
# @option_group(
#     'Available files to process',
#     option('--mucho', 'filename', flag_value=INDICES, help='Read all indices'),
#     option('-b', '--cobi', 'filename', flag_value=[INDICES[0]], help='Read cobifile'),
#     option('-h', '--cohp', 'filename', flag_value=[INDICES[1]], help='Read cohpfile'),
#     option('-o', '--coop', 'filename', flag_value=[INDICES[2]], help='Read coopfile'),
# )
# @cloup.option('-a', '--all', 'all', flag_value=True, help='Process all relevant files')
def process(dir_path, filetype, filename):
    # if dir_path == '.':
    #     print('amigo no me diste un directorio')
    print(f'Dirpath is {os.path.abspath(dir_path)}')
    print(f'Filetype is {filetype}')
    print(f'Filename is {filename}')
    # if filename == None:
    #     print('No filename flag specified')
    #     return

    # absolute_path = os.path.abspath(dir_path)

    # if file_exists(absolute_path, filename):
    #     print(f'{filename} is present in {absolute_path}')
    # else:
    #     print(f'{filename} is not present in {absolute_path}')


if __name__ == '__main__':
    process()

def file_exists(dir_path, filename):
    items = os.listdir(dir_path)
    return filename in items