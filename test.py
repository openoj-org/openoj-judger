data = {'language':'C++', 
    'src':'/Users/stian/Desktop/SE_OJ/Judger/src.cpp', 
    'max_cpu_time':10000,
    'max_memory':10*1024, 
    'test_case_input':['/Users/stian/Desktop/SE_OJ/Judger/input.in'], 
    'test_case_output':['/Users/stian/Desktop/SE_OJ/Judger/output.out']}

data = {'language':'C++', 
        'src':'/Users/stian/Desktop/SE_OJ/Judger/src/judger/tests/data/src.cpp', 'max_time':10000, 'max_memory':10000,
        'test_case_input':['/Users/stian/Desktop/SE_OJ/Judger/src/judger/tests/data/input.in'],
        'test_case_output':['/Users/stian/Desktop/SE_OJ/Judger/src/judger/tests/data/output.out']}
import os
cwd  = '/Users/stian/Desktop/SE_OJ/Judger/src/judger/tests/'
# # data = {'language':'C++', 
# #                 'src':os.path.join(cwd, 'data', 'wa.cpp'), 'max_time':10000, 'max_memory':10000,
# #                 'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
# #                 'test_case_output':[os.path.join(cwd, 'data', 'output.out')],
# #                 'use_docker':False}

# #subtask
# import base64
# with open(os.path.join(cwd, 'data', 'src.cpp'), 'rb') as f:
#         src = base64.b64encode(f.read()).decode()
# with open(os.path.join(cwd, 'data', 'input.in'), 'rb') as f:
#         input = base64.b64encode(f.read()).decode()
# with open(os.path.join(cwd, 'data', 'output.out'), 'rb') as f:
#         output = base64.b64encode(f.read()).decode()
# data = {'language':'C++', 
#         'src':src, 'max_time':10000, 'max_memory':10000,
#         'test_case_input':[[input], [input]],
#         'test_case_output':[[output], [output]],
#         'test_case_score':[50, 50]}
import requests
import json

import requests
response = requests.post('http://101.43.210.67:5000/submit_code', json=data)
print(response.text)
print(response.json())
import time
time.sleep(3)
response = requests.get(f'http://101.43.210.67:5000/get_result/{response.json()["id"]}')
# print(response.text)
# print(json.loads(response.text)["0"])
print(response.json())
print(type(response.json()))

