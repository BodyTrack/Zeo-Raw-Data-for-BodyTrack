#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char **argv)
{
  char *filename = argv[1];
  int fd = open(filename, O_RDONLY | O_NONBLOCK);
  FILE *in= fdopen(fd, "r");

  char buf[200];
  sprintf(buf, "stty -f %s 38400 -crtscts", filename);
  system(buf);

  fcntl(fd, F_SETFL, fcntl(fd, F_GETFL) | ~O_NONBLOCK);

  time_t t;
  time(&t);
  fprintf(stderr, "Capture starting at %s\n", ctime(&t));
  
  while (1) {
    int c = getc(in);
    if (c == EOF) break; // happens when there's an error reading, e.g. USB cable is unplugged
    putchar(c);
    fflush(stdout);
  }
  
  time(&t);
  fprintf(stderr, "Capture ending at %s\n", ctime(&t));

  return 0;
}
