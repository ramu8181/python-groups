#sum of the numbers in the list








# sum of the num


def findsum (n=1):
    if n == 1 or n == 0:
        return 1
    return n + findsum(n-1)



if __name__=='__main__':
    print (findsum(5))
