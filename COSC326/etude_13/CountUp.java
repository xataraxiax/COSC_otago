/**
    Etude 13: CountingUp
    File name: CountUp.java
    Authors: Stefan Pedersen 1427681, Jono Sue 4097307
    Date created: 01/02/2017
    Date last modified: 02/02/2017
*/

public class CountUp{

    //Assert statement to check for overflow in addition
    //Bitwise check code found at stackoverflow.com/questions/3001836
    //(User: Durandal, June 8, 2010)
    public static void additionCheck(long s, long d){
        long r = s + d;
        assert !(((s & d & ~r) | (~s & ~d & r)) < 0) :
            "Overflow in the addition of " + s + " and " + d;
    }

    //Finds binomial coefficient of each number from 0..n for each
    //number from 0..k, resulting in the construction of pascal's
    //triangle. Uses that triangle to find binomial coefficient for n,k.
    //Algorithm translated from python found at joequery.me/notes-on-dynamic
    //-programming-part-1/
    public static long binomial(int n, int k){
        long count[][] = new long[n+1][k+1];
        int i, j;
        int counter = 0;
        for (i=0; i<=n; i++){
            for (j=0; j<=min(i,k); j++){
                if(j==0 || j==i){
                    count[i][j] = 1;
                } else {
                    additionCheck(count[i-1][j-1], count[i-1][j]);
                    count[i][j] = count[i-1][j-1]+count[i-1][j];
                }
            counter ++;
            }
        }
        // System.out.println(counter + " additions performed");
        return count[n][k];
    }

    //helper method to check for minimum of a and b
    public static long min(int a, int b){
        return(a < b ? a : b);
    }

    public static void main(String[] args){
        if (args.length == 2) {
            assert(Integer.parseInt(args[1])>=0) : "k must be non-negative";
            System.out.println(binomial(Integer.parseInt(args[0]),
            Integer.parseInt(args[1])));
        }
    }
}
