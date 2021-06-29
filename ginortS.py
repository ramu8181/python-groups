# Enter your code here. Read input from STDIN. Print output to STDOUT
#input Sorting1234
#output ginortS1324

if __name__ == '__main__':
   string =  raw_input().strip()
   upper= []
   lower = []
   numbereven = []
   numberodd = []
   print string
   for i in string:
       if i.isupper():
           upper.append(i)
       elif i.islower():
           lower.append(i)
       elif i.isdigit() and int(i)%2==0:
           numbereven.append(i)
       elif i.isdigit() and int(i)%2!=0:
           numberodd.append(i) 
print(''.join(sorted(lower)) + ''.join(sorted(upper)) +''.join(sorted(numberodd)) +''.join(sorted(numbereven))) 
    