import re
import urllib.request

#targetURL= "http://www.gutenberg.org/files/48320/48320-0.txt"
#data = urllib.urlopen(target_url)
#for line in data: # files are iterable
#    print (line)
sher = 0
line = " "
res1 = ".*SHERLOCK\s+HOLMES.*"
res2 = ".*you\ssee,\sbut\syou\sdo\snot\sobserve.*"
res3 = ".*elementary, dear Watson"
sher,ob,wat = 0,0,0
with urllib.request.urlopen("http://www.gutenberg.org/files/48320/48320-0.txt") as url:
    s = url.readlines()
    print(type(s))
    s = [x.decode('utf-8').strip() for x in s if x!='']
    for i in range (0, len(s)-1,1):
       line =  s[i].upper()
#       print (line)
      # res1 = re.match(".*SHERLOCK\sHOLMES.*",line)
       if(re.match(res1,line)):
          print(line)
          sher += 1
       line =  s[i].lower()
       print (line)
       if(re.match(res2,line)):
          #print("We have a match!")
          ob += 1
       if(re.match(res3,line)):
          #print("We have a match!")
          wat += 1

print (sher)
print (ob)
print (wat)
       
