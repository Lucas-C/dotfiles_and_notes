/*
** SOLUTION by Zeldarck
*/
package com.isograd.exercise;
import java.util.ArrayList;
import java.util.Scanner;

public class IsoContest {
  public static void main( String[] argv ) throws Exception {
    String  line;
    Scanner sc = new Scanner(System.in);
    String[] tab = null;
    long res =0;
    int res2 = 0;
    int max = 0;

    line = sc.nextLine();    
    int n = Integer.parseInt(line);
    int[] poto = new int[n];

    int f=0;
    while(sc.hasNextLine()){
      line = sc.nextLine();    
      poto[f] = Integer.parseInt(line);            
      f++;
    }
    for(int i =0; i <n; i++){
      int taille = poto[i];
      for(int j = i+1; j<n; j++){
        if(poto[j] >taille){
          break;
        }
        if(poto[j] == taille){
          res += (j-i);
          break;
        }
      }
    }
    System.out.println(res + res2);
  }
}
