#include"util.h"

int run_tests_with_limits(const char* exe, const char* language, const int case_id, const int id, const int time_limit, const int memory_limit, const int stack_memory_limit) {
    // Set the resource limits
    struct rlimit memory_limit_rlim;
    memory_limit_rlim.rlim_cur = memory_limit * 1024;//TODO notice the unit
    memory_limit_rlim.rlim_max = memory_limit * 1024;
    setrlimit(RLIMIT_AS, &memory_limit_rlim);

    struct rlimit stack_memory_limit_rlim;
    stack_memory_limit_rlim.rlim_cur = stack_memory_limit * 1024;
    stack_memory_limit_rlim.rlim_max = stack_memory_limit * 1024;
    setrlimit(RLIMIT_STACK, &stack_memory_limit_rlim);

    //TODO set the redirect file here, add 2 input parameters
    char input_file_name[50];
    sprintf(input_file_name, "/tmp/%d/test_%d.in", id, case_id);
    char output_file_name[50];
    sprintf(output_file_name, "/tmp/%d/answer_%d.out", id, case_id);

    FILE* input = fopen(input_file_name, "r");
    if(input == NULL) {
        printf("Cannot open input file\n");
        return 1;
    }
    if(dup2(fileno(input), STDIN_FILENO) == -1) {
        printf("Cannot redirect stdin\n");
        return 1;
    }
    FILE* output = fopen(output_file_name, "w");
    if(output == NULL) {
        printf("Cannot open output file\n");
        return 1;
    }
    if(dup2(fileno(output), STDOUT_FILENO) == -1) {
        printf("Cannot redirect stdout\n");
        return 1;
    }

    execve(exe, NULL, NULL);
}