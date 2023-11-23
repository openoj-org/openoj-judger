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
    'max_cpu_time':10, #Timeout time, in ms
    'max_memory':2*1024, #Max stack size, in KB
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

## Bugs to fix

1. 目前采用Linux seccomp ulimit对stack size进行限制；但这样系统会将MLE处理成访问非法地址Segmentation Error，无法将MLE与Runtime Error进行区分了。
2. 在docker环境中使用unlimit 和 timeout存在未知错误，无法正常执行run script
3. 并发效率
4. 返回程序运行的 时间 和 内存 消耗
5. 优化source code和test cases的传入效率
6. Unknown Error
7. Spj
8. FLASK ~ backend

修改方式

1. 可以使用resource module限制栈内存、程序内存、对外部文件的访问、CPU time；需要一个外部的timer检测TLE；
2. 一种方法是开一个process跑user程序，一个process跑timer，parent process捕捉两个subprocess，使用wait4获取user程序的资源消耗；

最终修改方式：

由于seccomp和resource等python module存在各种问题（seccomp module在import时需要绑定系统API，在本机上安装失败；使用resource可以有效地限制测试程序的运行资源，但是如果搭配os.run/subprocess.run等方法，难以记录测试程序运行时消耗的资源，并且调试只能在Linux平台，MacOS上难以调用各种resource的API，而课程服务器连接不稳定，难以在服务器调试；加上考虑到python实现测试程序在高并发场景下或许会存在效率问题（未测试）），最终决定沙箱采用Linux secure computing mode (seccomp)实现，使用C实现，并提供接口供Python编写的judger调用。
