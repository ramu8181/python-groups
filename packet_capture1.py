import pyshark
import signal
import re

def run_program():
   """
   ...time consuming execution...
   """
   print ("Other Part of code can be handled")



def Exit_gracefully(signal, frame):
    """
    ... log exiting information ...
    ... close any open files ...
    """
    sys.exit(0)


def    capture_packet(interface_name,no_of_capture,port_capture):
    """
    ?????dns?
    timeout: ????????30s
    :return: capture dns?
    """
    interface = "en0"
    out_string = ""
    i =  1
    cap = pyshark.LiveCapture(interface=interface_name,bpf_filter=port_capture)
    cap.sniff(timeout=2)
    #for pkt in cap:
    for pkt in cap.sniff_continuously(packet_count=no_of_capture):
        out_file = open("Eavesdrop_Data.txt", "w")
        out_string += "Packet# " + str(i)
        out_string += "\n"
        out_string += str(pkt)
        out_string +=  "EOF"
        out_string += "\n"
        out_file.write(out_string)
        i = i + 1
    cap.close()


def  read_packet():
    """ Reading the packet  to display the contents"""
    main_list = []
    with open("Eavesdrop_Data.txt",'r+') as file:
       while True:
          data = file.readline()
          if not data:
             break   
          if (re.search("^Packet# ", data)): 
             lista = []
             while True:
                 data = file.readline()
                 if not data:
                    break
                 if (re.search("^EOF",data)):
                    break
                 else:
                     lista.append(data)
          main_list.append(lista)          
       return main_list


def process_packet(main_list):
    final_list = []
    for header in main_list:
       if ( isinstance (header, list)):
           list1 = []   
           for i in range (0,  len(header)):   
               if ( re.search ("^Layer\sETH:" , header[i])):
                  a,b = re.split('\s',header[i+1].strip())
                  list1.append(b)
                  a,b = re.split('\s',header[i+2].strip())
                  list1.append(b)
               if ( re.search ("^Layer\sIP:" , header[i])):
                   a,b = re.split('\s',header[i+17].strip())
                   list1.append(b)
                   a,b = re.split('\s',header[i+18].strip())
                   list1.append(b)
           final_list.append(list1)
    print("sr.                   dstMac                                  srcMac                                 SrcIP                    DestIP")
    j = 1
    for each in final_list:   
       print (str(j) + "                 " + str(each[0]) + "                  "  + str(each[1]) + "                      " + str(each[2]) + "                   "  + str(each[3]))
       j += 1                                                       
               
#(not(re.search("^EOF",file.readline()))):


if __name__ == '__main__':
   interface_name =  str(input("Enter the Interface name to be captured  "))
   no_of_capture =  int(input ("Enter the no of packets to be captured  "))
   port_capture =  input ("Enter the Port to be captured  ")
   capture_packet(interface_name,no_of_capture,port_capture)
   main_list = read_packet()
   #print (main_list)
   process_packet(main_list)
   run_program()

   
   
