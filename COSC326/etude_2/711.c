#include <stdio.h>

int main() {
    unsigned int A, B, C, D;
    unsigned int Aind, Bind, Cind;
    unsigned int divs [62] =
        {1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36,
          40, 45, 48, 50, 54, 60, 64, 72, 75, 80, 90, 96, 100, 108, 120, 125,
          135, 144, 150, 160, 180, 192, 200, 216, 225, 240, 250, 270,
          288, 300, 320, 360, 375, 400, 432, 450, 480, 500, 540, 576, 600, 625};
    for(Aind=0, A=divs[0]; Aind<62; Aind++, A=divs[Aind])

        for(Bind=0, B=divs[0]; A+B<=673 && Bind<=Aind; Bind++, B=divs[Bind])

            for(Cind=0, C=divs[0]; A+B+C<=674 && Cind<=Bind; Cind++, C=divs[Cind]) {
                D = 675 - (A+B+C);

                if(D<=C) {
                    if(A*B*C*D == 660000000) {
                        printf("A: %u, B: %u, C:%u, D: %u\n", A, B, C, D);
                    }
                }
            }
    return(1);
}
