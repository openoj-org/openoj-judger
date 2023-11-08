
import random
import os
import shutil
from config import *
from compiler import Compiler
from runner import Runner

test_case = {'language':'Python',
 'src':'''
if __name__ == '__main__':
    n = int(input())
    for i in range(n):
        line = input()
        a, b = line.split()
        a = int(a)
        b = int(b)
        print( a + b)
''',
'max_cpu_time':10,
'max_memory':128*1024*1024,
'test_case_input':'''3
1 2
2 2
0 1
''',
'test_case_output':'''3
4
1
''' }

def judge(data):
    """
    :param data: dict
    language, src, max_cpu_time, max_memory, test_case_input, test_case_output
    :return: dict
    """
    #mkdir
    id = random.randint(0, 100000)
    dir = os.path.join(WORKING_DIR, str(id))
    os.mkdir(dir)
    os.chdir(dir)
    print("working dir: " + dir)
    src_file = 'main' + suffix[data['language']]
    with open(src_file, 'w') as f:
        f.write(data['src'])
    with open('test.in', 'w') as f:
        f.write(data['test_case_input'])
    with open('test.out', 'w') as f:
        f.write(data['test_case_output'])

    #compile
    compiler = Compiler(src_file, data['language'])
    result = compiler.compile()
    print(result)
    if result['success'] == False:
        return {'success':False, 'error':result['error']}
    else:
        exe_path = result['exe_path']   

    #run
    runner = Runner(exe_path, data['language'], 'test.in', 'test.out', data['max_cpu_time'], data['max_memory'])
    result = runner.run()
    print(result)

    #clean
    os.chdir(WORKING_DIR)
    shutil.rmtree(str(id))

judge(test_case)

