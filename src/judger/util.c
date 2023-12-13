#include"util.h"

#ifdef __linux__
int load_seccomp_policy() {
    scmp_filter_ctx ctx = NULL;
    ctx = seccomp_init(SCMP_ACT_ALLOW);
    if (!ctx) {
        return 1;
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(clone), 0) != 0)
        return 1;
    if (seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(fork), 0) != 0)
        return 1;
    if (seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(vfork), 0) != 0)
        return 1;
    if (seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(kill), 0) != 0)
        return 1;
    // if (seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 1, SCMP_A0(SCMP_CMP_NE, (scmp_datum_t)(exe))) != 0)
    //     return 1;
    // Currently not support any write
    // if (seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(write), 0) != 0)
    //     return 1;
    // if (seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(writev), 0) != 0)
    //     return 1;
    
    // seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(write), 1, SCMP_CMP(0, SCMP_CMP_NE, STDOUT_FILENO));
    if (seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(write), 1, SCMP_CMP(0, SCMP_CMP_NE, STDOUT_FILENO)) != 0)
        return 1;
    
    if (seccomp_load(ctx) != 0) {
        return 1;
    }
    seccomp_release(ctx);
    return 0;
}
#endif
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
    #ifdef __linux__
    if (load_seccomp_policy() != 0) {
        perror("Failed to load seccomp policy\n");
        return 1;
    }
    #endif
    if(strcmp(language, "Python") == 0) {
        // execl("python3", "python3", "main.py", (char *)NULL);
        execlp("python3", "python3", exe, NULL);
    }
    else {
        execve(exe, NULL, NULL);
    }
    return 0;
}

