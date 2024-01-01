if __name__ == '__main__':
    n = input()
    with open('my_out.txt', "w") as f:
        f.write("This message should not be successfully written to the file")
    for i in range(int(n)):
        line = input()
        a = line.split()[0]
        b = line.split()[1]
        print(int(a) + int(b))