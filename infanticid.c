#include <stdio.h>
#include <unistd.h>
#include <getopt.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>

static int child_num, status, Index=0;
static pid_t child_pids[10000];


typedef struct stud_options {
    int WRITE_IP_OCTET;
    int WRITE_PROXY_LINE;
    const char* CHROOT;
    uid_t UID;
    gid_t GID;
    const char *FRONT_IP;
    const char *FRONT_PORT;
    const char *BACK_IP;
    const char *BACK_PORT;
    long NCORES;
    const char *CERT_FILE;
    const char *CIPHER_SUITE;
    const char *ENGINE;
    int BACKLOG;
#ifdef USE_SHARED_CACHE
    int SHARED_CACHE;
#endif
    int QUIET;
    int SYSLOG;
    int TCP_KEEPALIVE;
} stud_options;

static stud_options OPTIONS = {
    0,            // WRITE_IP_OCTET
    0,            // WRITE_PROXY_LINE
    NULL,         // CHROOT
    0,            // UID
    0,            // GID
    NULL,         // FRONT_IP
    "8443",       // FRONT_PORT
    "127.0.0.1",  // BACK_IP
    "8000",       // BACK_PORT
    2,            // NCORES
    NULL,         // CERT_FILE
    NULL,         // CIPHER_SUITE
    NULL,         // ENGINE
    100,          // BACKLOG
#ifdef USE_SHARED_CACHE
    0,            // SHARED_CACHE
#endif
    0,            // QUIET
    0,            // SYSLOG
    3600          // TCP_KEEPALIVE
};

static void fail(const char* s) {
    perror(s);
    exit(1);
}

/* Handle children process termination.
   Display error if needed but continue  and
   exits at the end of the list */
static void terminate_children()
{
int i=0;

    for ( i = 0; i < OPTIONS.NCORES; i++) {
        if (kill(child_pids[i],SIGTERM) < 0) {
	    perror("stud:terminate_children - ");
	    }
        }
    exit(0);
}

void init_signals() {
    struct sigaction act;

    sigemptyset(&act.sa_mask);
    act.sa_flags = 0;
    act.sa_handler = SIG_IGN;

    /* Avoid getting PIPE signal when writing to a closed file descriptor */
    if (sigaction(SIGPIPE, &act, NULL) < 0)
        fail("sigaction - sigpipe");

    /* We don't care if someone stops and starts a child process with kill (1) */
    act.sa_flags = SA_NOCLDSTOP;


    /* We do care when child processes change status */
    if (sigaction(SIGCHLD, &act, NULL) < 0)
        fail("sigaction - sigchld");
}


/* Enable specific SIGTERM handling by the parent proc
   It becomes responsible for terminating children. */
void handle_sigterm() {
    struct sigaction act;

    sigemptyset(&act.sa_mask);
    act.sa_flags = 0;

    act.sa_handler = terminate_children;

    if (sigaction(SIGTERM, &act, NULL) < 0)
        fail("sigaction - sigterm");
}

void usage(char *Prog)
{
printf("%s : -n Number of Children\n",Prog);
}

/* Forks COUNT children starting with START_INDEX.
 * Each child's index is stored in child_num and its pid is stored in child_pids[child_num]
 * so the parent can manage it later. */
void start_children(int start_index, int count) {
    for (child_num = start_index; child_num < start_index + count; child_num++) {
        int pid = fork();
        if (pid == -1) {
            printf("{core} fork() failed! Goodbye cruel world!\n");
            exit(1);
        }
        else if (pid == 0) { /* child */
            sleep(100000);
            exit(0);
        }
        else { /* parent. Track new child. */
	    printf("Started child with pid = %d\n",pid);
            child_pids[child_num] = pid;
        }
    }
}

main(int argc, char **argv)
{
int c=0, FatherStatus;

init_signals();

    while (1) {
        int option_index = 0;
        c = getopt(argc, argv, "n:");

        if (c == -1)
            break;

        switch (c) {

        case 'n':
            OPTIONS.NCORES=atoi(optarg);
            break;

        default:
            usage(argv[0]);
        }
    }

    printf("Number of children to be started : %d\n",(int)OPTIONS.NCORES);
    start_children(Index,OPTIONS.NCORES);
    handle_sigterm();
    wait(&FatherStatus);

}
