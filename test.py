from src.judger.judger import judge
# data = {'language':'C++', 'src':'/Users/stian/Desktop/SE_OJ/Judger/tests/test.cpp', 'max_cpu_time':10, 'max_memory':1024*1024*1024, 'test_case_input':['/Users/stian/Desktop/SE_OJ/Judger/tests/test.in'], 'test_case_output':['/Users/stian/Desktop/SE_OJ/Judger/tests/test.out']}
# res = judge(data)
# print(res)

data = {'language':'Python', 'src':'/Users/stian/Desktop/SE_OJ/Judger/tests/test.py', 'max_cpu_time':10, 'max_memory':1024*1024*1024, 'test_case_input':['/Users/stian/Desktop/SE_OJ/Judger/tests/test.in'], 'test_case_output':['/Users/stian/Desktop/SE_OJ/Judger/tests/test.out']}
res = judge(data)
print(res)