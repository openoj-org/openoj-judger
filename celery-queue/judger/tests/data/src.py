if __name__ == '__main__':
    n = input()
    for i in range(int(n)):
        line = input()
        a = line.split()[0]
        b = line.split()[1]
        print(int(a) + int(b))