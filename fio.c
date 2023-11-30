#include<stdio.h>

int main() {
    FILE* input = fopen("/Users/stian/Desktop/SE_OJ/Judger/buffer.txt", "w");
    if(input == NULL) {
        printf("Cannot open input file\n");
        return 1;
    }
    fprintf(input, "1 2 3 4 5 6 7 8 9 10");
    fclose(input);
    return 0;
}