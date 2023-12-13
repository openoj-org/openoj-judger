import unittest
from ..judger import judge
import os
import logging


class TestMyModule(unittest.TestCase):
    def test_API_judge_Python(self):
        print("test_write_Python")
        cwd = os.path.dirname(os.path.abspath(__file__))
        data = {'language':'Python', 
                'src':os.path.join(cwd, 'data', 'src_write.py'), 'max_time':10000, 'max_memory':10000,
                'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
                'test_case_output':[os.path.join(cwd, 'data', 'output.out')],
                'use_docker':False}
        result = judge(data)
        self.assertEqual(result['success'], False)

    def test_API_judge_Cpp(self):
        print("test_write_Cpp")
        cwd = os.path.dirname(os.path.abspath(__file__))
        data = {'language':'C++', 
                'src':os.path.join(cwd, 'data', 'src_write.cpp'), 'max_time':10000, 'max_memory':10000,
                'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
                'test_case_output':[os.path.join(cwd, 'data', 'output.out')],
                'use_docker':False}
        result = judge(data)
        self.assertEqual(result['success'], False)

if __name__ == '__main__':
    unittest.main()