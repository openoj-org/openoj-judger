import unittest
from ..judger import judge, judge_entrance
import os
import logging


class TestMyModule(unittest.TestCase):
    def test_MLE(self):
        print("test_MLE")
        cwd = os.path.dirname(os.path.abspath(__file__))
        data = {'language':'C++', 
                'src':os.path.join(cwd, 'data', 'mle.cpp'), 'max_time':10000, 'max_memory':5000,
                'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
                'test_case_output':[os.path.join(cwd, 'data', 'output.out')],
                'use_docker':False}
        result = judge(data)
        print(result)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['0']['error_type'], 'MLE')
    
if __name__ == '__main__':
    unittest.main()