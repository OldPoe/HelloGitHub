from math import sqrt  
def isprime(n):  
    k = int(sqrt(n))  
    for i in range(2,k+1):  
        if n % i == 0:  
            return 0  
    return 1  
      
if __name__ == '__main__':  
    for n in range(101, 201):  
        if isprime(n) ==1:  
            print(n, end = ' ')  
