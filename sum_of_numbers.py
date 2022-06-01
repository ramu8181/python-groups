#sum of the numbers in the list, this is iterative method and uses the 

if __name__=='__main__':
    N = int(input("Enter the Integer"))
    j = 0 
    for i in range (0,N):
        j = j+ i
    print (j)






# sum of the num


def findsum (n=1):
    if n == 1 or n == 0:
        return 1
    return n + findsum(n-1)



if __name__=='__main__':
    print (findsum(5))
