import unittest
from ..judger import judge
import os
import logging


class TestMyModule(unittest.TestCase):
    def test_API_judge_Python(self):
        print("test_API_judge_Python")
        cwd = os.path.dirname(os.path.abspath(__file__))
        data = {'language':'Python', 
                'src':os.path.join(cwd, 'data', 'src.py'), 'max_time':10000, 'max_memory':10000,
                'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
                'test_case_output':[os.path.join(cwd, 'data', 'output.out')],
                'use_docker':False}
        result = judge(data)
        self.assertEqual(result['success'], True)

    def test_API_judge_Cpp(self):
        print("test_API_judge_Cpp")
        cwd = os.path.dirname(os.path.abspath(__file__))
        data = {'language':'C++', 
                'src':os.path.join(cwd, 'data', 'src.cpp'), 'max_time':10000, 'max_memory':10000,
                'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
                'test_case_output':[os.path.join(cwd, 'data', 'output.out')],
                'use_docker':False}
        result = judge(data)
        self.assertEqual(result['success'], True)

    def test_TLE(self):
        print("test_TLE")
        cwd = os.path.dirname(os.path.abspath(__file__))
        data = {'language':'C++', 
                'src':os.path.join(cwd, 'data', 'src.cpp'), 'max_time':10, 'max_memory':10000,
                'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
                'test_case_output':[os.path.join(cwd, 'data', 'output.out')],
                'use_docker':False}
        result = judge(data)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['error_type'], 'TLE')

    def test_WA(self):
        print("test_WA")
        cwd = os.path.dirname(os.path.abspath(__file__))
        data = {'language':'C++', 
                'src':os.path.join(cwd, 'data', 'wa.cpp'), 'max_time':10000, 'max_memory':10000,
                'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
                'test_case_output':[os.path.join(cwd, 'data', 'output.out')],
                'use_docker':False}
        result = judge(data)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['error_type'], 'WA')

    def test_MLE(self):
        print("test_MLE")
        cwd = os.path.dirname(os.path.abspath(__file__))
        data = {'language':'C++', 
                'src':os.path.join(cwd, 'data', 'mle.cpp'), 'max_time':10000, 'max_memory':10,
                'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
                'test_case_output':[os.path.join(cwd, 'data', 'output.out')],
                'use_docker':False}
        result = judge(data)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['error_type'], 'MLE')
    
if __name__ == '__main__':
    unittest.main()