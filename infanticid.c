#include <stdio.h>
#include <unistd.h>
#include <getopt.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>

static int child_num, status, Index=0;
static pid_t child_pids[10000];

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
int NumChild=2, c=0, FatherStatus;

    while (1) {
        int option_index = 0;
        c = getopt(argc, argv, "n:");

        if (c == -1)
            break;

        switch (c) {

        case 'n':
            NumChild=atoi(optarg);
            break;

        default:
            usage(argv[0]);
        }
    }

    printf("Number of children to be started : %d\n",NumChild);
    start_children(Index,NumChild);
    wait(&FatherStatus);

}
