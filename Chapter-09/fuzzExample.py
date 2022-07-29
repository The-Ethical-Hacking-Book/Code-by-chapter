import sys
import afl 
import os

#-----------------------------------------
#   Place test function here
#-----------------------------------------

def main():
    in_str = sys.stdin.read()
    a, b, c = in_str.strip().split(" ")
    a = int(a)
    b = int(b)
    c = int(c)

	testFunction(a,b,c)

if __name__ == "__main__": 
    afl.init()       
    main()
    os._exit(0)

 

def test(x):
    c = q*p #Two large primes. 
    if(pow(2,x) % c == 17):
        print("Error")
    else:
        print("No Error")


#include <stdio.h>

void checkPass(int x){
	if(x == 7857){
		printf("Access Granted");	
	}else{
		printf("Access Denied");
	}
}

int main(int argc, char *argv[]) { 
	int x = 0; 	
	printf("Enter the password: ");
  	scanf("%d", &x);
	checkPass(x);
}
