#include <stdio.h>

int main(int argc, char **argv)
{
  char buf[1000];
  int i;
  for (i=0; i<5; i++) fgets(buf, sizeof(buf), stdin);
  while (1) {
    int n;
    if (1 != fscanf(stdin, "%x", &n)) break;
    putchar(n);
  }
  return 0;
}
