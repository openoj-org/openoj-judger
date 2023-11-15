import unittest
from ..judger import judge
import os

class TestMyModule(unittest.TestCase):
    def test_API_judge_Python(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        data = {'language':'Python', 
                'src':os.path.join(cwd, 'data', 'src.py'), 'max_cpu_time':10, 'max_memory':128*1024*1024,
                'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
                'test_case_output':[os.path.join(cwd, 'data', 'output.out')]}
        result = judge(data)
        self.assertEqual(result['success'], True)

    def test_API_judge_Cpp(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        data = {'language':'C++', 
                'src':os.path.join(cwd, 'data', 'src.cpp'), 'max_cpu_time':10, 'max_memory':128*1024*1024,
                'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
                'test_case_output':[os.path.join(cwd, 'data', 'output.out')]}
        result = judge(data)
        self.assertEqual(result['success'], True)

if __name__ == '__main__':
    unittest.main()