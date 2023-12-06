# data = {'language':'C++', 
#     'src':'/Users/stian/Desktop/SE_OJ/Judger/src.cpp', 
#     'max_cpu_time':10000,
#     'max_memory':10*1024, 
#     'test_case_input':['/Users/stian/Desktop/SE_OJ/Judger/input.in'], 
#     'test_case_output':['/Users/stian/Desktop/SE_OJ/Judger/output.out']}
data = {'language':'C++', 
        'src':'/Users/stian/Desktop/SE_OJ/Judger/src/judger/tests/data/src.cpp', 'max_time':10000, 'max_memory':10000,
        'test_case_input':['/Users/stian/Desktop/SE_OJ/Judger/src/judger/tests/data/input.in'],
        'test_case_output':['/Users/stian/Desktop/SE_OJ/Judger/src/judger/tests/data/output.out']}
import requests
import json

import requests
response = requests.post('http://127.0.0.1:5000/judger', json=data)
print(response.text)

