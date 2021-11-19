
### to Install the deepdiff run this command pip install 'deepdiff[murmur]'

from deepdiff import DeepDiff
from pprint import pprint

def verify(file_name):
   dict1 = {}
   rt_name = ""
   routeinfo =  []
   with open(file_name) as file_1:
      file_1_text = file_1.readlines()
   for each in file_1_text:
      if  "Routing Table:" in each:
         temp = each.split(":")
         if (not (rt_name and rt_name.strip())):
           rt_name = temp[1].strip()
           routeinfo = []
         else:
           dict1[rt_name] = routeinfo
           rt_name = temp[1].strip()
           routeinfo = []
         #print(rt_name)
      elif ("B" in each ):
         temp = each.split(" ")
         filter_object = filter(lambda x: x != "", temp)
         without_empty_strings = list(filter_object)
         routeinfo.append(without_empty_strings[1])
         #print (routeinfo)
   #print(dict1)
   return dict1





if __name__=='__main__':
   dict1 = verify("file1.txt")
   dict2 = verify("file11.txt") 
   for (key,value), (key1,value1) in zip(dict1.items(), dict2.items()):
     if (key == key1):
       if (len(value) != len(value1)):
         #pprint ( "VRF is modified   " + str(key))
         #pprint ( "OLD_VALUE = " + str(value))
         #pprint ( "NEW_VALUE = " + str(value1))
         modified = set(value).difference(set(value1))
         if ( len(modified)):
           pprint ( "VRF is modified   " + str(key))
           pprint (modified)
         
   
   diff = DeepDiff(dict1,dict2)
   #pprint (diff,indent=2)