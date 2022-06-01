

print("Hello World")


def findsum (n=1):
    if n == 1 or n == 0:
        return 1
    return n + findsum(n-1)


def fibonacci(n=2):
    if n == 0 or n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)
if __name__=='__main__':
    print (fibonacci(5))
