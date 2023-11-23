from judger.judger import judge

# data = {'language':'Python', 
#     'src':'/Users/stian/Desktop/SE_OJ/Judger/src.py', 
#     'max_cpu_time':10,
#     'max_memory':1024*1024*1024, 
#     'test_case_input':['/Users/stian/Desktop/SE_OJ/Judger/input.in'], 
#     'test_case_output':['/Users/stian/Desktop/SE_OJ/Judger/output.out']}
# res = judge(data)
# print(res)

data = {'language':'C++', 
    'src':'/Users/stian/Desktop/SE_OJ/Judger/src.cpp', 
    'max_cpu_time':10,
    'max_memory':10*1024, 
    'test_case_input':['/Users/stian/Desktop/SE_OJ/Judger/input.in'], 
    'test_case_output':['/Users/stian/Desktop/SE_OJ/Judger/output.out']}
res = judge(data)
print(res)