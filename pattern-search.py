# Python code to search .dat files in current
# folder (We can change file type/name and path
# according to the requirements.
import os
import subprocess
import re
# This is to get the directory that the program
# is currently running in.
#dir_path = os.path.dirname(os.path.realpath(__file__))

def finding_dir_path():
   dir_path = "/opt/versa/vnms/apache-tomcat/webapps/versa/app/docs/rest"
   new_file=open("/var/tmp/filepath.txt",mode="w")
   for root, dirs, files in os.walk(dir_path):
      for file in files:
         if file.endswith('api_data.js'):
            print (root+'/'+str(file))
            new_file.write(root+"/"+str(file)+"\n")

def processing_rest_api():
   with open("/var/tmp/filepath.txt","r") as f1:
      list1 = list(f1.readlines())
      list1 = [x.strip() for x in list1]
      for each in list1:
         with open(each,"r") as f2:
            list2 = list(f2.readlines())
            list2 = [x.strip() for x in list2]
            for i in range (0 ,len(list2)):
               if re.match("\"type\":\s\"GET|PUT|POST|DELETE|PATCH\"",list2[i]):
                  print (each)
                  print (list2[i])
                  print (list2[i+1])
                  print (list2[i+2])


if __name__=='__main__':
    finding_dir_path()
    processing_rest_api()
