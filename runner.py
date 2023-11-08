import os
import subprocess
import time
import threading
import hashlib


class Runner:
    def __init__(self, exe, language, input, output, timeout, max_memory) -> None:
        self.exe = exe
        self.language = language
        self.input = input
        self.output = output
        self.timeout = timeout
        self.max_memory = max_memory

    def run(self):
        if self.language == 'C++' or self.language == 'C':
            return self.run_cpp()
        elif self.language == 'Java':
            return self.run_java()
        elif self.language == 'Python':
            return self.run_python()
        else:
            return {'success': False, 'error': 'Language not supported'}
        
    def run_cpp(self):
        cmd = 'ulimit -s {} ; ./{} < {}'.format(self.max_memory, self.exe, self.input)
        return self._run(cmd)
    
    def run_python(self):
        cmd = 'ulimit -s {} ; python3 {} < {} '.format(self.max_memory, self.exe, self.input)
        return self._run(cmd)

    def _run(self, cmd):
        try:
            p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, timeout=self.timeout)
            # p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=self.timeout)
            # out, err = p.communicate()
            err = p.stderr
            out = p.stdout.decode('utf-8')
            if p.returncode != 0:
                return {'success': False, 'error': err.decode('utf-8')}
            
            user = hashlib.md5(out.rstrip().encode('utf-8')).hexdigest()
            with open(self.output, 'r') as f:
                answer = hashlib.md5(f.read().rstrip().encode('utf-8')).hexdigest()
            
            if user != answer:
                return {'success': False, 'error': 'Wrong Answer'}
            else:
                return {'success': True}

        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'TLE'}
        except subprocess.CalledProcessError:
            return {'success': False, 'error': 'subprocess.CalledProcessError'}