import random as rand
import sys
#-----------------------------------------
#    Place Test function here
#-----------------------------------------

def main():
	while True:
       a = rand.randint(-200, 200)
		b = rand.randint(-200, 200)
		c = rand.randint(-200, 200)
		print(a,b,c)
		testFunction(a,b,c)


if __name__ == "__main__": 
	main()