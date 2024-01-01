import subprocess
import os
from .config import DEFAULT_TMP_PATH, IMAGE

class Compiler:
    def __init__(self, src_path, language, id, is_spj=False):
        self.language = language                               
        self.src_path = os.path.join(DEFAULT_TMP_PATH, str(id), src_path)
        self.exe_path = os.path.join(DEFAULT_TMP_PATH, str(id), 'main') if not is_spj else os.path.join(DEFAULT_TMP_PATH, str(id), 'spj')
        self.id = id
        self.absolute_dir_path = os.path.dirname(os.path.abspath(__file__))

    def compile(self):
        if self.language == 'C':
            return self.compile_c()
        elif (self.language == 'C++') or (self.language == 'C++11'):
            return self.compile_cpp()
        elif self.language == 'Java':
            return self.compile_java()
        elif (self.language == 'Python') or (self.language == 'Python3'):
            return self.compile_python()
        else:
            return False
    
    def compile_c(self):
        cmd = 'gcc -o {} {} -Wall -lm -O2 -std=c99 -DONLINE_JUDGE -I{}'.format(self.exe_path, self.src_path, self.absolute_dir_path)
        return self._compile(cmd)
    
    def compile_cpp(self):
        cmd = 'g++ -o {} {} -Wall -lm -O2 -std=c++11 -DONLINE_JUDGE -I{}'.format(self.exe_path, self.src_path, self.absolute_dir_path)
        return self._compile(cmd)
    
    def compile_java(self):
        cmd = 'javac {} -d .'.format(self.src_path)
        return self._compile(cmd)
    
    def compile_python(self):
        cmd = 'python3 -m py_compile {}'.format(self.src_path)
        return self._compile(cmd)
    
    def _compile(self, cmd):
        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if p.returncode != 0:
                return {'success':False, 'error_type':"CE"}

            if self.language == 'C' or self.language == 'C++' or self.language == 'C++11':
                return {'success':True, 'exe_path':self.exe_path.split('/')[-1]}
            elif self.language == 'Java':
                return {'success':False, 'error_type':"CE"} # Current not support Java
            elif (self.language == 'Python') or (self.language == 'Python3'):
                pwd = os.getcwd()
                os.chdir(os.path.join(DEFAULT_TMP_PATH, str(self.id)))
                if os.path.exists('__pycache__') and os.path.isdir('__pycache__'):
                    exe_path = os.path.join('__pycache__', os.listdir('__pycache__')[0])
                    os.chdir(pwd)
                    return {'success':True, 'exe_path':exe_path}
                else:
                    os.chdir(pwd)
                    return {'success':False, 'error':'__pycache__ not found'}
        except subprocess.CalledProcessError:
            return {'success':False, 'error':'subprocess.CalledProcessError'}