import subprocess
import os

class Compiler:
    def __init__(self, src_path, language):
        self.src_path = src_path
        self.language = language
        self.exe_path = 'main'


    def compile(self):
        if self.language == 'C':
            return self.compile_c()
        elif self.language == 'C++':
            return self.compile_cpp()
        elif self.language == 'Java':
            return self.compile_java()
        elif self.language == 'Python':
            return self.compile_python()
        else:
            return False
    
    def compile_c(self):
        cmd = 'gcc -o {} {} -Wall -lm -O2 -std=c99 --static -DONLINE_JUDGE'.format(self.exe_path, self.src_path)
        return self._compile(cmd)
    
    def compile_cpp(self):
        cmd = 'g++ -o {} {} -Wall -lm -O2 -std=c++11 --static -DONLINE_JUDGE'.format(self.exe_path, self.src_path)
        # cmd = 'g++ -o {} {} -Wall -O2 -std=c++11'.format(self.exe_path, self.src_path)
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
                return {'success':False, 'error':err.decode('utf-8')}
            
            
            if self.language == 'C' or self.language == 'C++':
                return {'success':True, 'exe_path':self.exe_path}
            elif self.language == 'Java':
                pass #TODO
            elif self.language == 'Python':
                if os.path.exists('__pycache__') and os.path.isdir('__pycache__'):
                    exe_path = os.listdir('__pycache__')[0]
                    exe_path = os.path.join('__pycache__', exe_path)
                    return {'success':True, 'exe_path':exe_path}
                else:
                    return {'success':False, 'error':'__pycache__ not found'}
        except subprocess.CalledProcessError:
            return {'success':False, 'error':'subprocess.CalledProcessError'}