test_case = {'language':'Python',
 'src':'''
if __name__ == '__main__':
    n = int(input())
    for i in range(n):
        line = input()
        a, b = line.split()
        a = int(a)
        b = int(b)
        print( a + b)
''',
'max_cpu_time':10,
'max_memory':128*1024*1024,
'test_case_input':'''3
1 2
2 2
0 1
''',
'test_case_output':'''3
4
1
''' }