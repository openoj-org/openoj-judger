#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sched.h>
#include <signal.h>
#include <pthread.h>
#include <errno.h>
#include <unistd.h>

#include <sys/wait.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <sys/types.h>

#define DEFAULT_TMP_PATH "/tmp"


int run_tests_with_limits(const char* exe, const char* language, const int case_id, const int id, const int time_limit, const int memory_limit, const int stack_memory_limit);