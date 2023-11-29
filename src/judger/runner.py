import os
import subprocess
import time
import threading
import hashlib
import docker
from .config import DEFAULT_TMP_PATH, IMAGE, _ok, _wa
from .util import prepare_logger

class Runner:
    def __init__(self, exe, language, case_id, id, timeout=10, max_memory=1024*1024*128, use_docker=True, use_spj=False, spj_path=None) -> None:
        self.language = language
        self.use_docker = use_docker
        self.exe = os.path.join(DEFAULT_TMP_PATH, str(id), exe)
        self.input = os.path.join(DEFAULT_TMP_PATH, str(id), f'test_{case_id}.in')
        self.output = os.path.join(DEFAULT_TMP_PATH, str(id), f'test_{case_id}.out')

        self.timeout = timeout
        self.max_memory = max_memory
        self.use_docker = use_docker
        self.logger = prepare_logger()

        self.case_id = case_id
        self.id = id
        self.use_spj = use_spj
        self.spj_path = os.path.join(DEFAULT_TMP_PATH, str(id), spj_path) if spj_path else None
        if self.use_spj:
            assert self.spj_path is not None

        self.status, self.time_usage, self.memory_usage = None, None, None

    def run(self):
        if not self.use_docker:
            self.logger.info(f'Using the Crunner')
            
            path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(path, 'crunner')
            p = subprocess.run(f"{path} {self.exe} {self.language} {self.case_id} {self.id} {self.timeout} {self.max_memory} {self.max_memory}".split())
            self.logger.info(f'returncode: {p.returncode}')

            with open(f'{DEFAULT_TMP_PATH}/{self.id}/analysis_{self.case_id}.txt', 'r') as f:
                analysis = f.read()
            # 3 lines in analysis, decompose them into 3 vars
            analysis = analysis.rstrip().split('\n')
            self.status, self.time_usage, self.memory_usage = analysis[0], float(analysis[1]), int(analysis[2])
            if self.status != "OK":
                return {'success': False, 'error_type': self.status, 'time_usage': self.time_usage, 'memory_usage': self.memory_usage}

            if self.use_spj:
                return self._spj_run()
            else:
                return self._normal_run()
    
    def _normal_run(self):
        with open(f'{DEFAULT_TMP_PATH}/{self.id}/answer_{self.case_id}.out', 'r') as f:
            out = f.read()
        
        user = hashlib.md5(out.rstrip().encode('utf-8')).hexdigest()
        with open(self.output, 'r') as f:
            answer = hashlib.md5(f.read().rstrip().encode('utf-8')).hexdigest()
        
        if user != answer:
            return {'success': False, 'error_type':'WA', 'time_usage': self.time_usage, 'memory_usage': self.memory_usage}
        else:
            return {'success': True, 'time_usage': self.time_usage, 'memory_usage': self.memory_usage}

    def _spj_run(self):
        with open(f'{DEFAULT_TMP_PATH}/{self.id}/answer_{self.case_id}.out', 'r') as f:
            out = f.read()
        
        p = subprocess.Popen(f"{self.spj_path} {f'{DEFAULT_TMP_PATH}/{self.id}/test_{self.case_id}.in'} {f'{DEFAULT_TMP_PATH}/{self.id}/answer_{self.case_id}.out'} {f'{DEFAULT_TMP_PATH}/{self.id}/test_{self.case_id}.out'}",
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # TODO check returncode p
        flag = p.stdout.read().decode('utf-8').rstrip().split()[0]
        if flag == 'ok':
            return {'success': True, 'time_usage': self.time_usage, 'memory_usage': self.memory_usage}
        elif flag == 'wrong':
            return {'success': False, 'error_type':'WA', 'time_usage': self.time_usage, 'memory_usage': self.memory_usage}
        else:
            #TODO
            pass
        
        