import os
import subprocess
import time
import threading
import hashlib
import docker
from .config import DEFAULT_TMP_PATH, IMAGE

class Runner:
    def __init__(self, exe, language, case_id, id, timeout=10, max_memory=1024*1024*128) -> None:
        self.exe = os.path.join(str(id), exe)
        self.language = language
        self.input = os.path.join(str(id), f'test_{case_id}.in')
        self.output = os.path.join(str(id), f'test_{case_id}.out')
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
        # cmd = 'ulimit -s {} ; {} < {}'.format(self.max_memory, self.exe, self.input)
        cmd = '{} < {}'.format(self.exe, os.path.join(DEFAULT_TMP_PATH, self.input))
        return self._run(cmd)
    
    def run_python(self):
        # cmd = 'ulimit -s {} ; python3 {} < {} '.format(self.max_memory, self.exe, self.input)
        cmd = 'python3 {} < {} '.format(self.exe, os.path.join(DEFAULT_TMP_PATH, self.input))
        return self._run(cmd)

    def _run(self, cmd):
        # try:
        # try:
        #     client = docker.from_env()
        #     volumes = {DEFAULT_TMP_PATH: {'bind': '/home', 'mode': 'rw'}}
        #     out = client.containers.run(IMAGE, cmd, volumes=volumes, remove=True)
        # except docker.errors.ContainerError as e:
        #     return {'success': False, 'error_type': 'Compilation Error','error': e.stderr.decode('utf-8')}

        # subprocess ver.--------------------------------------
        docker_prefix = f"docker run -i -v {DEFAULT_TMP_PATH}:/home {IMAGE} "
        p = subprocess.run(docker_prefix + cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, timeout=self.timeout)
        err = p.stderr.decode('utf-8')
        out = p.stdout.decode('utf-8')
        if p.returncode != 0:
            return {'success': False, 'error': err}
        # -----------------------------------------------------
        
        user = hashlib.md5(out.rstrip().encode('utf-8')).hexdigest()
        with open(os.path.join(DEFAULT_TMP_PATH, self.output), 'r') as f:
            answer = hashlib.md5(f.read().rstrip().encode('utf-8')).hexdigest()
        
        if user != answer:
            return {'success': False, 'error_type':'WA', 'error': 'Wrong Answer'}
        else:
            return {'success': True}

    #TODO test errors
    # except subprocess.TimeoutExpired:
    #     return {'success': False, 'error': 'TLE'}
    # except subprocess.CalledProcessError:
    #     return {'success': False, 'error': 'subprocess.CalledProcessError'}