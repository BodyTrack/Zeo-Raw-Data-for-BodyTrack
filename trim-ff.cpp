#include <stdio.h>

int main(int argc, char **argv)
{
  int ff_count = 0;
  while (1) {
    int c = getchar();
    if (c == EOF) break;
    if (c == 0xff) ff_count++;
    else {
      for(; ff_count; ff_count--) { putchar(0xff); }
      putchar(c);
    }
  }
}
