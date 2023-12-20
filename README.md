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

## Start the service

`celery -A app.celery worker --loglevel=info`

`flask run`

## API (TODO)

return structure

多个测试点(Multiple test cases)

success：bool, If all test cases are passed, return True; otherwise False;

score: total score obtained;

"i" : ith test case result, including "memory_usage", "success", "time_usage", "error_type"

Example: {"0":{"memory_usage":1196032,"success":true,"time_usage":1566},"score":100,"success":true}

多个子任务 (Multiple subtasks)

success：bool, If all subtasks are passed, return True; otherwise False;

score: total score obtained;

"i" : ith subtask result, the same to the multiple test cases result, excluding "score".

Example: {'0': {'0': {'success': True, 'time_usage': 700, 'memory_usage': 1196032}, 'success': True}, '1': {'0': {'success': True, 'time_usage': 240, 'memory_usage': 1196032}, 'success': True}, 'score': 100, 'success': True}

## Run tests

In the directory `src`, run

`python3 -m unittest judger.tests.test_e2e`

`python3 -m unittest judger.tests.test_spj`

## Bugs to fix

* [X] 目前采用Linux seccomp ulimit对stack size进行限制；但这样系统会将MLE处理成访问非法地址Segmentation Error，无法将MLE与Runtime Error进行区分了。
* [X] 在docker环境中使用unlimit 和 timeout存在未知错误，无法正常执行run script
* [X] 并发效率 (基于redis celery实现了消息队列)
* [X] 返回程序运行的 时间 和 内存 消耗
* [ ] 优化source code和test cases的传入效率
* [ ] Unknown Error
* [X] Spj
* [X] FLASK ~ backend (input API)
* [ ] Test on Linux platform
  * [ ] 问题1：wait4返回的资源消耗与valgrinder检测到的不一样，后者大20倍 (有可能是中途异常退出的情况下，两个方法的处理方法不同；尝试一下success的测例的情况)
  * [ ] 问题2：当内存限制从小到大，依次出现cannot open input file, bad acclocate, AC
* [X] Restrict the directory that the user exe can visit (128MB)
  尝试了几种方法。
  第一种：使用chroot + execvl，好处是都是基础的linux syscall，但是问题在于chroot后，新的root下连bash都没有；即使把bash复制过来，也需要把所有的动态链接库都复制过来，这样需要用到Linux Namespace，类似于docker的实现思路；
  第二种：使用SELinux，编写一个policy来限制资源访问；不过在服务器上安装失败；(后来发现是Ubuntu不支持SELinux，需要使用AppArmor)
  第三种：使用seccomp，编写一个policy；这是最终选取的方式，不过存在问题，在子进程中限制write后，父进程中的write也被限制了，无法为子进程重定向标准输出到answer.out中。
* [X] A script that compile the package (C part) and install necessary packages

修改方式

1. 可以使用resource module限制栈内存、程序内存、对外部文件的访问、CPU time；需要一个外部的timer检测TLE；
2. 一种方法是开一个process跑user程序，一个process跑timer，parent process捕捉两个subprocess，使用wait4获取user程序的资源消耗；

最终修改方式：

由于seccomp和resource等python module存在各种问题（seccomp module在import时需要绑定系统API，在本机上安装失败；使用resource可以有效地限制测试程序的运行资源，但是如果搭配os.run/subprocess.run等方法，难以记录测试程序运行时消耗的资源，并且调试只能在Linux平台，MacOS上难以调用各种resource的API，而课程服务器连接不稳定，难以在服务器调试；加上考虑到python实现测试程序在高并发场景下或许会存在效率问题（未测试）），最终决定沙箱采用Linux secure computing mode (seccomp)实现，使用C实现，并提供接口供Python编写的judger调用。
