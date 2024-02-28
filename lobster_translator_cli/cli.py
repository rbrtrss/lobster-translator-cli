import click
import os

@click.command()
@click.argument('dir_path', type=click.Path(exists=True))
@click.option('-b', '--cobi', 'filename', flag_value='COBICAR.lobster', help='Read cobifile')
@click.option('-h', '--cohp', 'filename', flag_value='COHPCAR.lobster', help='Read cohpfile')
@click.option('-o', '--coop', 'filename', flag_value='COOPCAR.lobster', help='Read coopfile')
@click.option('-a', '--all', 'all', flag_value=True, help='Process all relevant files')
def process(dir_path, filename, all):
    # if dir_path == '.':
    #     click.echo('amigo no me diste un directorio')
    if filename == None:
        click.echo('No filename specified')
        return
    
    if all:
        click.echo('Va todo eh')

    absolute_path = os.path.abspath(dir_path)

    if file_exists(absolute_path, filename):
        click.echo(f'{filename} is present in {absolute_path}')
    else:
        click.echo(f'{filename} is not present in {absolute_path}')


if __name__ == '__main__':
    process()

def file_exists(dir_path, filename):
    items = os.listdir(dir_path)
    return filename in items