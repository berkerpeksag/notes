#include <stdio.h>

int main(void)
{
    char ch = 'c';
    char *chptr = &ch;

    int i = 20;
    int *intptr = &i;

    char *ptr = "I am\0a string"; /* %s will read from *ptr (which is I) to \0 */

    /*
     * Output:
     *
     * *chptr: [c], *intptr: [20], *ptr: [I], (*ptr+1): [J], (*ptr+2): [K],
     * *(ptr+2): [a], ptr: [I am a string]
     *
     */
    printf("*chptr: [%c], *intptr: [%d], *ptr: [%c], "
           "(*ptr+1): [%c], (*ptr+2): [%c], *(ptr+2): [%c], ptr: [%s]\n",
           *chptr, *intptr, *ptr, (*ptr+1), (*ptr+2), *(ptr+2), ptr);

    return 0;
}
