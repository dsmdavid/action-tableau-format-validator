import inspect
import sys
import os
from functools import wraps
from log import MyLogger, logger_levels

logger = MyLogger(log_file='style-check.log', log_path='logs', name=__name__)

def log_start(func):
    @wraps(func)
    def call(*arg, **kwargs):
        logger.debug(f'Starting function {func.__name__}')
        return func(*arg, **kwargs)
    return call 
@log_start
def get_modified_files():
    # this file is created from an upstream action
    with open('./github/workspace/modified_files.txt','r') as f:
        files = f.read().replace('"','')
    file_list = []
    for file in files.split(' '):
        file_list.extend(file.split())
    return file_list
@log_start
def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)
@log_start
def get_path_to_guide():
    '''Returns the actual path to the style guide based on action input'''
    path_to_json = os.environ.get('PATH_TO_JSON')
    if path_to_json:
        logger.debug(f'Path_to_json: {path_to_json}')
        return os.path.join('/github/workspace/', path_to_json)
    else:
        logger.error('Style guide was not found')
        print('::error ::The style guide was not found')

    sys.exit(1)

if __name__ == '__main__':
    logger.info('Start script')
    logger.debug('Setting logger levels')

    logger_level = os.environ.get('INPUT_LOGGER_LEVEL', 'INFO')
    logger_set_level = logger_levels.get(logger_level, logger_levels['INFO'])
    print(f'The logger level provided was {logger_level}. This will be set: {logger_set_level}')
    logger.setLevel(logger_set_level)
    try:
        modified_files = get_modified_files()
    except:
        sys.exit()
    path_to_json = get_path_to_guide()
    logger.debug(f'The initial list of files {modified_files}')
    modified_files = list(filter(lambda x: 'twb' in x, modified_files))
    logger.debug(f'The twb files are:\n {modified_files}')
    print(modified_files)
    commands = []
    for file in modified_files:
        logger.debug(f'--- Testing file {file}') 
        filepath = os.path.join('/github/workspace', file)
        logger.debug(f'filepath: {filepath}')
        path_src = get_script_dir()
        path_src = os.path.join(path_src, 'validator_cli.py')
        command = ' '.join(["python", f"{path_src}","--style-guide",path_to_json, f"--tableau-workbook {filepath}", ">> ./github/workspace/outputs.txt"])
        commands.append(f"echo 'processing {filepath}' >> ./github/workspace/outputs.txt")
        commands.append(command)
        logger.debug(f'command: {command}')

        logger.debug('---end testing---')
    text = '#!/bin/bash\n' +'echo Starting\n' + '\n'.join(commands) + '\necho Showing outputs:\n' + '\ncat ./github/workspace/outputs.txt\n'
    path_to_commands = os.path.join(os.getcwd(), 'commands.sh')
    print(f'Saving commands to {path_to_commands}')
    with open(path_to_commands,'w') as f:
        f.writelines(text)
    print(f'Commands saved to {path_to_commands}')
