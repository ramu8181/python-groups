import re


#Program to write the files for the top networking devices to find the list

if __name__=='__main__':
   network_devices = {}
   traffic_a = []
   with open ("status.txt", 'r') as f:
       content = f.readlines()
       content = [ x.strip() for x in content]
       for i in range (len(content)):
          list_get = content[i].split(',')
          if ( list_get[0] in network_devices):
              temp = network_devices[list_get[0]] + list_get[2] + list_get[3]
              network_devices[list_get[0]] = temp
          else:
              network_devices[list_get[0]] =  list_get[2] + list_get[3]
       print (network_devices)
       traffic_a = sorted(network_devices, key=network_devices.get , reverse=False)
       print (traffic_a)