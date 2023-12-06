import random
import os
import shutil
from .config import *
from .compiler import Compiler
from .runner import Runner
from .util import prepare_logger
logger = prepare_logger()

def copy_source_code(data, id):
    src_file = 'main' + suffix[data['language']]
    path = os.path.join(DEFAULT_TMP_PATH, str(id), src_file)
    if isinstance(data['src'], bytes):
        with open(path, "wb") as f:
            f.write(data['src'])
    elif isinstance(data['src'], str):
        shutil.copy(data['src'], path)
    else:
        raise TypeError("data['src'] should be bytes or str")
    return src_file

def copy_spj_code(data, id):
    src_file = 'spj' + suffix[data['spj_language']]
    path = os.path.join(DEFAULT_TMP_PATH, str(id), src_file)
    if isinstance(data['spj_src'], bytes):
        with open(path, "wb") as f:
            f.write(data['spj_src'])
    elif isinstance(data['spj_src'], str):
        shutil.copy(data['spj_src'], path)
    else:
        raise TypeError("data['spj_src'] should be bytes or str")
    return src_file

def copy_test_cases(data, id):
    if isinstance(data['test_case_input'], list) and isinstance(data['test_case_output'], list):
        if len(data['test_case_input']) != len(data['test_case_output']):
            raise ValueError("data['test_case_input'] and data['test_case_output'] should have the same length")
        for idx, (test_input, test_output) in enumerate(zip(data['test_case_input'], data['test_case_output'])):
            if type(test_input) != type(test_output):
                raise TypeError("elements of data['test_case_input'] and data['test_case_output'] should be the same type")
            if isinstance(test_input, bytes):
                with open(os.path.join(DEFAULT_TMP_PATH, str(id), f'test_{idx}.in'), 'wb') as f:
                    f.write(test_input)
                with open(os.path.join(DEFAULT_TMP_PATH, str(id), f'test_{idx}.out'), 'wb') as f:
                    f.write(test_output)
            elif isinstance(test_input, str):
                shutil.copy(test_input, os.path.join(DEFAULT_TMP_PATH, str(id), f'test_{idx}.in'))
                shutil.copy(test_output, os.path.join(DEFAULT_TMP_PATH, str(id), f'test_{idx}.out'))
            else:
                raise TypeError("elements of data['test_case_input'] and data['test_case_output'] should be bytes or str")
    else:
        raise TypeError("data['test_case_input']and data['test_case_output'] should be a list")

# class Data:
    # def __init__(self, language, src, test_case_input, test_case_output, max_time, max_memory, use_spj, spj_language) -> None:
        

def judge(data):
    """
    :param data: dict
    language, src, max_time, max_memory, test_case_input, test_case_output
        - language: str, 'C', 'C++', 'Java', 'Python'
        - src: bytes(bytes of source code) or str(absolute path of source code)
        - spj_src: bytes(bytes of source code) or str(absolute path of source code)
        - test_case_input: (list of) bytes(bytes of test case input) or str(absolute path of test case input)
        - test_case_output:(list of) bytes(bytes of test case output) or str(absolute path of test case output)
        - max_time: int, in ms
        - max_memory: int, in KB
    :return: dict
    """
    #mkdir
    id = random.randint(0, 100000)
    dir = os.path.join(DEFAULT_TMP_PATH, str(id))
    os.mkdir(dir)
    logger.info("Working dir: " + dir)  # e.g. /tmp/12345
    
    #copy source code and test cases to working dir
    src_file = copy_source_code(data, id)  # main.cpp
    copy_test_cases(data, id)
    if data.get('use_spj', False):
        spj_file = copy_spj_code(data, id)

    #compile
    logger.info("Compiling user source code...")
    compiler = Compiler(src_file, data['language'], id, data.get('use_docker', False))
    result = compiler.compile()
    logger.info(result)
    if result['success'] == False:
        return result
    else:
        exe_path = result['exe_path'] # main
    
    if data.get('use_spj', False):
        logger.info("Compiling spj source code...")
        spj_compiler = Compiler(spj_file, data['spj_language'], id, data.get('use_docker', False), is_spj=True)
        spj_result = spj_compiler.compile()
        logger.info(spj_result)
        if spj_result['success'] == False:
            return spj_result
        else:
            spj_exe_path = spj_result['exe_path']
    else:
        spj_exe_path = None

    #run
    logger.info("Running...")
    for idx in range(len(data['test_case_input'])):
        runner = Runner(exe_path, data['language'], idx, id, data['max_time'], data['max_memory'], data.get('use_docker', False), data.get('use_spj', False), spj_exe_path)
        result = runner.run()
        if not result['success']:
            result['error_case'] = idx
            return result

    #clean
    shutil.rmtree(dir)
    return result


