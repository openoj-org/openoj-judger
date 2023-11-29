import unittest
from ..judger import judge
import os
import logging


class TestMyModule(unittest.TestCase):
    def test_spj(self):
        print("test_spj")
        cwd = os.path.dirname(os.path.abspath(__file__))
        data = {'language':'C++', 
                'src':os.path.join(cwd, 'data', 'src.cpp'), 'max_cpu_time':10000, 'max_memory':10000,
                'test_case_input':[os.path.join(cwd, 'data', 'input.in')],
                'test_case_output':[os.path.join(cwd, 'data', 'output.out')],
                'use_docker':False,
                'use_spj':True,
                'spj_language':'C++',
                'spj_src':os.path.join(cwd, 'data', 'spj.cpp')}
        result = judge(data)
        self.assertEqual(result['success'], True)

if __name__ == '__main__':
    unittest.main()