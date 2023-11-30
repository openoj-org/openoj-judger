#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == -1) {
        perror("fork");
        exit(EXIT_FAILURE);
    }

    if (pid == 0) {
        // 子进程

        // 切换到指定目录
        if (chdir("/Users/stian/Desktop/SE_OJ/Judger/ojTrash") != 0) {
            perror("chdir");
            exit(EXIT_FAILURE);
        }

        // 切换根目录
        if (chroot("/Users/stian/Desktop/SE_OJ/Judger/ojTrash") != 0) {
            perror("chroot");
            exit(EXIT_FAILURE);
        }

        // 设置uid和gid，可以使用具有限制权限的用户
        if (setuid(1000) != 0 || setgid(1000) != 0) {
            perror("setuid/setgid");
            exit(EXIT_FAILURE);
        }

        // 执行外部程序
        execl("/Users/stian/Desktop/SE_OJ/Judger/fio", "/Users/stian/Desktop/SE_OJ/Judger/fio", NULL);

        // 如果execl执行失败
        perror("execl");
        exit(EXIT_FAILURE);
    } else {
        // 等待子进程结束
        waitpid(pid, NULL, 0);
    }

    return 0;
}
