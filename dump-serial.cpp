#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
  char *filename = argv[1];
  int fd = open(filename, O_RDONLY | O_NONBLOCK);
  FILE *in= fdopen(fd, "r");

  char buf[200];
  sprintf(buf, "stty -f %s 38400 -crtscts", filename);
  system(buf);
  sprintf(buf, "stty -f %s", filename);
  system(buf);

  fcntl(fd, F_SETFL, fcntl(fd, F_GETFL) | ~O_NONBLOCK);
  
  while (1) {
    int c = getc(in);
    putchar(c);
    fflush(stdout);
  }
}
