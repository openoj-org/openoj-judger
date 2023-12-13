import unittest
from ..judger import judge, judge_entrance
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
                'src':os.path.join(cwd, 'data', 'src.cpp'), 'max_time':1, 'max_memory':10000,
                'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
                'test_case_output':[os.path.join(cwd, 'data', 'output.out')],
                'use_docker':False}
        result = judge(data)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['0']['error_type'], 'TLE')

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
        self.assertEqual(result['0']['error_type'], 'WA')

    def test_binary(self):
        print("test_binary")
        cwd = os.path.dirname(os.path.abspath(__file__))
        import base64
        with open(os.path.join(cwd, 'data', 'src.cpp'), 'rb') as f:
            src = base64.b64encode(f.read()).decode()
        with open(os.path.join(cwd, 'data', 'input.in'), 'rb') as f:
            input = base64.b64encode(f.read()).decode()
        with open(os.path.join(cwd, 'data', 'output.out'), 'rb') as f:
            output = base64.b64encode(f.read()).decode()
        data = {'language':'C++', 
                'src':src, 'max_time':10000, 'max_memory':10000,
                'test_case_input':[input],
                'test_case_output':[output],
                'test_case_score':[100]}
        result = judge(data)
        self.assertEqual(result['success'], True)
        self.assertEqual(result['score'], 100)

    def test_subtask(self):
        print("test_subtask")
        cwd = os.path.dirname(os.path.abspath(__file__))
        import base64
        with open(os.path.join(cwd, 'data', 'src.cpp'), 'rb') as f:
            src = base64.b64encode(f.read()).decode()
        with open(os.path.join(cwd, 'data', 'input.in'), 'rb') as f:
            input = base64.b64encode(f.read()).decode()
        with open(os.path.join(cwd, 'data', 'output.out'), 'rb') as f:
            output = base64.b64encode(f.read()).decode()
        data = {'language':'C++', 
                'src':src, 'max_time':10000, 'max_memory':10000,
                'test_case_input':[[input], [input]],
                'test_case_output':[[output], [output]],
                'test_case_score':[50, 50]}
        result = judge_entrance(data)
        self.assertEqual(result['success'], True)
        self.assertEqual(result['score'], 100)
    
if __name__ == '__main__':
    unittest.main()