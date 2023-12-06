#include "util.h"

int child_pid = 0;

void timer_handler(int signum) {
    if (signum == SIGALRM) {
        kill(child_pid, SIGKILL);
        printf("Time limit exceeded, killed the process.\n");
    }
}

int main(int argc, char *argv[]) {
    if (argc != 8) {
        printf("Usage: %s <exe> <language> <case_id> <id> <time_limit> <memory_limit> <stack_memory_limit>\n", argv[0]);
        return 1;
    }
    const char *exe = argv[1];
    const char *language = argv[2];
    const int case_id = atoi(argv[3]);
    const int id = atoi(argv[4]);

    const int time_limit = atoi(argv[5]);
    const int memory_limit = atoi(argv[6]);
    const int stack_memory_limit = atoi(argv[7]);

    // Fork 
    pid_t pid = fork();
    if (pid == -1) {
        perror("Fork failed\n");
        return 1;
    }

    if (pid == 0) {
        // Child process
        // Load seccomp policy
        #ifdef __linux__
        if (load_seccomp_policy() != 0) {
            perror("Failed to load seccomp policy\n");
            return 1;
        }
        #endif
        run_tests_with_limits(exe, language, case_id, id, time_limit, memory_limit, stack_memory_limit); //TODO
    }
    else {
        // Parent process
        // Make a timer, and kill the child process if it exceeds the time limit
        child_pid = pid;
        if (signal(SIGALRM, timer_handler) == SIG_ERR) {
            perror("Failed to register signal handler");
            return EXIT_FAILURE;
        }

        struct itimerval timer;
        timer.it_value.tv_sec = time_limit / 1000;
        timer.it_value.tv_usec = (time_limit % 1000) * 1000;
        timer.it_interval.tv_sec = 0;
        timer.it_interval.tv_usec = 0;

        setitimer(ITIMER_REAL, &timer, NULL);


        struct timeval start_time, end_time;
        double elapsed_time;
        gettimeofday(&start_time, NULL);

        int status;
        struct rusage usage;
        // Wait for the child process to finish; use wait4 in order to get resource usage
        wait4(pid, &status, 0, &usage);
        timer.it_value.tv_sec = 0;
        timer.it_value.tv_usec = 0;
        setitimer(ITIMER_REAL, &timer, NULL);

        gettimeofday(&end_time, NULL);

        const double cpu_time_used = usage.ru_utime.tv_sec * 1000 + usage.ru_utime.tv_usec / 1000; // in ms
        elapsed_time = (end_time.tv_sec - start_time.tv_sec) * 1000 +(end_time.tv_usec - start_time.tv_usec) / 1000;
        const int memory_used = usage.ru_maxrss; // in KB
        
        printf("CPU Time used: %f ms\n", cpu_time_used);
        printf("Real Time used: %f ms\n", elapsed_time);
        printf("Memory used: %d KB\n", memory_used);

        //Open a file called analysis_%d.txt id and write the analysis result into it
        char analysis_file_name[50];
        sprintf(analysis_file_name, "/tmp/%d/analysis_%d.txt", id, case_id);
        FILE *analysis_file = fopen(analysis_file_name, "w");
        if (analysis_file == NULL) {
            printf("Failed to open analysis file\n");
            return 1;
        }
        // fprintf(analysis_file, "%f\n", cpu_time_used);

        if (WIFSIGNALED(status)) {
            // Get the signal number
            const int signal = WTERMSIG(status);
            if(signal == SIGSEGV && memory_used > memory_limit) {
                printf("Memory limit exceeded\n");
                fprintf(analysis_file, "MLE\n");
            }
            else if (signal == SIGKILL) {
                printf("Time limit exceeded\n");
                fprintf(analysis_file, "TLE\n");
            }
            else {
                printf("Runtime error\n");
                fprintf(analysis_file, "RE\n");
            }
            fprintf(analysis_file, "%f\n", elapsed_time);
            fprintf(analysis_file, "%d\n", memory_used);
            fclose(analysis_file);
            return 0;
        }
        else {
            printf("OK\n");
            fprintf(analysis_file, "OK\n");
            fprintf(analysis_file, "%f\n", elapsed_time);
            fprintf(analysis_file, "%d\n", memory_used);
            fclose(analysis_file);
            return 0;
        }
    }
    return 0;
}
