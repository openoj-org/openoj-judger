import os
import subprocess
import time
import threading
import hashlib
import docker
from .config import DEFAULT_TMP_PATH, IMAGE
from .util import prepare_logger

class Runner:
    def __init__(self, exe, language, case_id, id, timeout=10, max_memory=1024*1024*128, use_docker=True) -> None:
        self.language = language
        self.use_docker = use_docker
        if self.use_docker:
            self.exe = os.path.join(DEFAULT_TMP_PATH, str(id), exe)
            self.input = os.path.join(DEFAULT_TMP_PATH, str(id), f'test_{case_id}.in')
            self.output = os.path.join(DEFAULT_TMP_PATH, str(id), f'test_{case_id}.out')
        else:
            self.exe = os.path.join(DEFAULT_TMP_PATH, str(id), exe)
            self.input = os.path.join(DEFAULT_TMP_PATH, str(id), f'test_{case_id}.in')
            self.output = os.path.join(DEFAULT_TMP_PATH, str(id), f'test_{case_id}.out')
        self.timeout = timeout
        self.max_memory = max_memory
        self.use_docker = use_docker
        self.logger = prepare_logger()

        self.case_id = case_id
        self.id = id

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
        cmd = 'ulimit -s {} ; {} < {}'.format(self.max_memory, self.exe, self.input)
        # cmd = '{} < {}'.format(self.exe, self.input)
        return self._run(cmd)
    
    def run_python(self):
        cmd = 'ulimit -s {} ; python3 {} < {} '.format(self.max_memory, self.exe, self.input)
        # cmd = 'python3 {} < {} '.format(self.exe, self.input)
        return self._run(cmd)

    def _run(self, cmd):
        if not self.use_docker:
            self.logger.info(f'Using the Crunner')
            # try:
            #     client = docker.from_env()
            #     volumes = {DEFAULT_TMP_PATH: {'bind': '/home', 'mode': 'rw'}}
            #     out = client.containers.run(IMAGE, cmd, volumes=volumes, remove=True)
            # except docker.errors.ContainerError as e:
            #     return {'success': False, 'error_type': 'Docker Error','error': e.stderr.decode('utf-8')}
            
            #Get the absolute path of this file (not include the file name)
            path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(path, 'crunner')
            p = subprocess.run(f"{path} {self.exe} {self.language} {self.case_id} {self.id} {self.timeout} {self.max_memory} {self.max_memory}".split())
            self.logger.info(f'returncode: {p.returncode}')
            with open(f'{DEFAULT_TMP_PATH}/{self.id}/answer_{self.case_id}.out', 'r') as f:
                out = f.read()
            with open(f'{DEFAULT_TMP_PATH}/{self.id}/analysis_{self.case_id}.txt', 'r') as f:
                analysis = f.read()
            
            # 4 lines in analysis, decompose them into 4 vars
            analysis = analysis.rstrip().split('\n')
            status, time_usage, memory_usage = analysis[0], float(analysis[1]), int(analysis[2])
            if status != "OK":
                return {'success': False, 'error_type': status, 'time_usage': time_usage, 'memory_usage': memory_usage}
        # subprocess ver.-----------------------------------------------------
        else:
            self.logger.info(f'Running {cmd} in subprocess')
            docker_prefix = f"docker run -i -v {DEFAULT_TMP_PATH}:/home {IMAGE} "
            # p = subprocess.run(docker_prefix + cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, timeout=self.timeout)
            try:
                p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, timeout=self.timeout)
                err = p.stderr.decode('utf-8')
                out = p.stdout.decode('utf-8')
                if p.returncode != 0:
                    if 'Segmentation fault' in err:
                        return {'success': False, 'error_type': 'MLE', 'error': err}
                    return {'success': False, 'error_type': 'MLE','error': err}
            except subprocess.TimeoutExpired:
                return {'success': False, 'error_type': 'TLE', 'error': 'Time Limit Exceeded'}
            except subprocess.CalledProcessError:
                return {'success': False, 'error_type': 'subprocess error', 'error': 'subprocess.CalledProcessError'}
        # -----------------------------------------------------
        
        user = hashlib.md5(out.rstrip().encode('utf-8')).hexdigest()
        with open(self.output, 'r') as f:
            answer = hashlib.md5(f.read().rstrip().encode('utf-8')).hexdigest()
        
        if user != answer:
            return {'success': False, 'error_type':'WA', 'time_usage': time_usage, 'memory_usage': memory_usage}
        else:
            return {'success': True, 'time_usage': time_usage, 'memory_usage': memory_usage}
