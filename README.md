# openoj-judger

A python package to simply judge your code.

## Usage quickstart
First, setup the docker image and judger package.
```shell
chmod +x ./setup.sh
./setup.sh
```

Then, you can import the package in your project like the following code.

```python
from judger.judger import judge

data = {'language':'Python', 
    'src':'/Users/stian/Desktop/SE_OJ/Judger/src.py',  #Both absolute path of source file or exact file in the type of <bytes> are supported.
    'max_cpu_time':10, #Timeout time, in seconds
    'max_memory':1024*1024*1024, #Max stack size, in bytes
    'test_case_input':['/Users/stian/Desktop/SE_OJ/Judger/input.in'], # Must be list, it can be list of absolute path of files or exact files in the type of <bytes>.
    'test_case_output':['/Users/stian/Desktop/SE_OJ/Judger/output.out']} # Must be list, it can be list of absolute path of files or exact files in the type of <bytes>.
res = judge(data)
print(res)

# Possible return value:

# >>> {'success': True}
# >>> {'success': False, 'error_type': 'Compilation Error', 'error': detailed error message from stderr...}
# >>> {'success': False, 'error_type': 'WA', 'error': 'Wrong Answer'}
# >>> {'success': False, 'error_type': 'TLE', 'error': detailed error message from stderr...}
```

## API (TODO)