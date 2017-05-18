/**
Etude 5: Numbers
File name: num1.c
Authors: Jono Sue 4097307, Stefan Pedersen 1427681
Date created: 23/01/2017
Date last modified: 29/01/2017
**/

#define check1(e) check1_(e, #e, x)
#define check2(e) check2_(e, #e, x, y)
#define _XOPEN_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

// Perform bitwise operations to safely calculate a midpoint without
// risk of overflow.
static int midpt(int x, int y){
    return (x & y) + ((x ^ y) >> 1);
}

static int min(int x, int y) {
    return x < y ? x : y;
}

static int max(int x, int y) {
    return x > y ? x : y;
}

static void check1_(int e, char const *s, int x) {
    if (!e) {
        fprintf(stderr, "%s failed for x = %d\n", s, x);
        abort();
    }
}

static void check2_(int e, char const *s, int x, int y) {
    if (!e) {
        fprintf(stderr, "%s failed for x = %d y = %d\n", s, x, y);
        abort();
    }
}

int main(){
    // TESTS. Failure of any will abort program.
    int numTests = 10000000;
    for (int i = 0; i < numTests; i++) {
        int const x = lrand48();
        int const y = lrand48();

        //check that the midpoint of x and x is itself x
        check1( midpt(x, x) == x );

        //check that the midpoint between x and -x is 0
        check1( midpt(x, -x) == 0 );

        //check that the midpoint between x and 0 is half of x
        check1( midpt(x, 0) == x/2 );

        //check that if x<=y then x <= midpt(x, y) <= y
        check2( min(x, y) <= midpt(x, y) );
        check2( midpt(x, y) <= max(x, y) );

        //check for symmetricality
        check2( midpt(x, y) == midpt(y, x));
    }
    printf("All checks passed on %d random numbers\n", numTests);
    return 0;
}
