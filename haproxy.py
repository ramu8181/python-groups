# Author Ramki
# HA Proxy Script which Does the Rest API Query and writes the master information in the Haproxy config file.
# Re-Validates and Restarts the HaProxy Event.

import requests
import json
import re
import logging
import os
import subprocess
import smtplib
import netmiko

from netmiko import ConnectHandler
from email.mime.text import MIMEText

def verify_debug_status(dir_ip):
    """ Runs the Debugger and Returns the HA Status.
    """
    list_edit = []
    device =ConnectHandler( device_type="flexvnf",ip=dir_ip,username="admin",password="versa123")
    your_string=device.send_command("show devices list")
    list_edit.append(your_string)
    your_string=device.send_command("show system package-info")
    list_edit.append(your_string)
    your_string=device.send_command("request vnmsha actions status")
    list_edit.append(your_string)
    if "SLAVE" in your_string:
           your_string=device.send_command("request vnmsha actions fail-over")
           list_edit.append(your_string)
           your_string=device.send_command("request vnmsha actions get-vnmsha-details fetch-peer-vnmsha-details true")
           list_edit.append(your_string)
    return list_edit



def verify_ha_status(dir1):
     """ Verifying the HA status and Returns the HA Status.
     """
     if (re.search("MASTER",dir1,re.MULTILINE)):
       dir_status = "MASTER"
     elif (re.search("SLAVE",dir1,re.MULTILINE)):
       dir_status = "SLAVE"
     else:
       dir_status = "Null"
     return dir_status


def email_sent(subject,description):
   """ Email is sent with Subject & Description which is sent calling proc
       """
   port = 587
   sender = 'ramkiversa@gmail.com'
   receiver = 'ramakrishnans@versa-networks.com'
   msg = MIMEText(description)
   msg['Subject'] = subject
   msg['From'] = sender
   msg['To'] = receiver
   user = 'ramkiversa@gmail.com'
   password = "ramu123?"

   with smtplib.SMTP("smtp.gmail.com", port ) as server:
      server.starttls() # Secure the connection
      server.login(user, password)
      server.sendmail(sender, receiver, msg.as_string())
      logging.info("Email successfully sent on the Event")


def rest_api_query(dir_ip_address):
    ha_status = {}
    for dir1_ip in dir_ip_address:
       try:
          logging.info (" The Display The package Information of the Director "+ dir1_ip)
          URL = "https://" + dir1_ip + ":9182/api/operational/system/package-info"
          post = requests.get(url=URL, auth=('Administrator', 'Versa@123'),
                verify=False, headers={'accept': 'application/json'})
          logging.info(json.dumps(post.json(), indent=4))

          dir1 = "https://" + dir1_ip + ":9182/api/config/vnmsha/actions/_operations/status"
          post = requests.post(url=dir1, auth=('Administrator', 'Versa@123'),
              verify=False, headers={'accept': 'application/json'})
          stat = json.dumps(post.json(), indent=4)
          dir1_status = verify_ha_status(stat)
          logging.info(dir1_status)
          ha_status[dir1_ip] = dir1_status
       except:
          logging.error ("Connection Error on the IP " + dir1_ip)
          ha_status[dir1_ip] = "Null"
    return ha_status

def update_ha_proxy_script(ha_prox_ip):
    try:
      sudoPassword = "versa123"
      file_name = "chmod 777 /etc/haproxy/haproxy.cfg"
      subprocess.getoutput('echo %s|sudo -S %s' % (sudoPassword,file_name))
      new_file=open("/etc/haproxy/haproxy.cfg",mode="w",encoding="utf-8")
      new_file.write("global\n")
      new_file.write("\tlog /dev/log    local0\n")
      new_file.write("\tlog /dev/log    local1 notice\n")
      new_file.write("\tchroot /var/lib/haproxy\n")
      new_file.write("\tstats socket /run/haproxy/admin.sock mode 660 level admin\n")
      new_file.write("\tstats timeout 30s\n")
      new_file.write("\tuser haproxy\n")
      new_file.write("\tgroup haproxy\n")
      new_file.write("\tdaemon\n")
      new_file.write("\t# Default SSL material locations\n")
      new_file.write("\tca-base /etc/ssl/certs\n")
      new_file.write("\tcrt-base /etc/ssl/private\n")
      new_file.write("\t# Default ciphers to use on SSL-enabled listening sockets.\n")
      new_file.write("\t# For more errorrmation, see ciphers(1SSL). This list is from:\n")
      new_file.write("\t#https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/\n")
      new_file.write("\tssl-default-bind-ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256::RSA+AES:RSA+3DES:!aNULL:!MD5:!DSS\n")
      new_file.write("\tssl-default-bind-options no-sslv3\n")
      new_file.write(" \n")
      new_file.write("defaults\n")
      new_file.write("\tlog\tglobal\n")
      new_file.write("\t mode\ttcp\n")
      new_file.write("\toption\ttcplog\n")
      new_file.write("\toption\tdontlognull\n")
      new_file.write("\ttimeout connect 5000\n")
      new_file.write("\ttimeout client  50000\n")
      new_file.write("\ttimeout server  50000\n")
      new_file.write("\terrorfile 400 /etc/haproxy/errors/400.http\n")
      new_file.write("\terrorfile 403 /etc/haproxy/errors/403.http\n")
      new_file.write("\terrorfile 408 /etc/haproxy/errors/408.http\n")
      new_file.write("\terrorfile 500 /etc/haproxy/errors/500.http\n")
      new_file.write("\terrorfile 502 /etc/haproxy/errors/502.http\n")
      new_file.write("\terrorfile 503 /etc/haproxy/errors/503.http\n")
      new_file.write("\terrorfile 504 /etc/haproxy/errors/504.http\n")
      new_file.write("frontend Local_Server\n")
      new_file.write("\tbind 10.192.216.154:443\n")
      new_file.write("\tmode tcp\n")
      new_file.write("\toption tcplog\n")
      new_file.write("\tdefault_backend versa_directors\n")
      new_file.write("backend versa_directors\n")
      new_file.write("\tmode tcp\n")
      new_file.write("\tbalance first\n")
      new_file.write("\tserver vd1.example.com  " + ha_prox_ip + ":443 check inter 2m downinter 2m observe layer4 error-limit 10 on-error mark-do
wn\n")
      new_file.write("listen stats\n")
      new_file.write("\tbind *:443\n")
      new_file.write("\toption httpchk HEAD /v1/sys/health\n")
      new_file.write("\thttp-check expect status 200\n")
      new_file.write("\toption tcplog\n")
      new_file.write("\toption redispatch\n")
      new_file.write("\tserver vd1.example.com " + ha_prox_ip +":443\n")
      new_file.close()
      proc = subprocess.getoutput('echo %s|sudo -S %s' % (sudoPassword,"haproxy -c -f /etc/haproxy/haproxy.cfg" ))
      print(proc)
      if "Error" in proc:
        logging.error("Configuration File is Invalid")
        logging.error(proc)
      elif "ALERT" in proc:
        logging.info("Configuration File is valid and Few Alert Errors")
        logging.info(proc)
      proc = subprocess.getoutput('echo %s|sudo -S %s' % (sudoPassword,"service haproxy restart " ))
      print(proc)
      if "Error" in proc:
        logging.error("Service Restart is throwing Error")
        logging.error(proc)
    except:
      logging.error("Error Opening the File to write the New Master Information")

    print (ha_prox_ip)
    return True

def verify_ha_proxy_script(ha_prox_ip):
    pattern = re.compile(ha_prox_ip)
    for i, line in enumerate(open('/etc/haproxy/haproxy.cfg')):
        for match in re.finditer(pattern, line):
            #print ('Found on line %s: %s' % (i+1, match.group()))
            return match.group()
    return False

if __name__=='__main__':
    try:
       logging.basicConfig(filename='/var/tmp/ha_proxy_event.log',level='INFO', filemode= 'a', format='%(asctime)s-%(name)s - %(levelname)s - %(m
essage)s')
    except:
       print ("The Logging Functionality is failed")
       exit()
    logging.info("Logging of the HAPROXY  Process Started")
    dir_ip_address = [ "210.1.1.3", "210.1.1.4"]
    preferred_master = ""
    ha_status = rest_api_query(dir_ip_address)
    logging.info(ha_status)
    print (ha_status)
    if ((ha_status[dir_ip_address[0]]  == ha_status[dir_ip_address[1]]) and (ha_status[dir_ip_address[0]] == "MASTER")):
        logging.error("Both the Directors in the split brain Scenario returning the Preferred Director")
        email_sent("Versa Director in Split Brain","Both the Directors in the split brain Scenario returning the Preferred Director")
        preferred_master = ha_status[dir_ip_address[0]]
    elif ((ha_status[dir_ip_address[0]]  == ha_status[dir_ip_address[1]]) and (ha_status[dir_ip_address[0]] == "Null")):
        logging.error("Both the Directors are not rechable hence exiting the script")
        email_sent("Versa Director are not Reachable","Both the Versa Directors are not Reachable")
        exit()
    elif (ha_status[dir_ip_address[0]] == "MASTER"):
        logging.info("Director is Master " + dir_ip_address[0])
        if dir_ip_address[0] == verify_ha_proxy_script(dir_ip_address[0]):
            logging.info("Config File changes not Required")
        else:
             logging.debug("HA MasterShip is Changed, Write Process")
             update_ha_proxy_script(dir_ip_address[0])
    elif (ha_status[dir_ip_address[1]] == "MASTER"):
        logging.info("Director is Master " + dir_ip_address[1])
        if dir_ip_address[1] == verify_ha_proxy_script(dir_ip_address[1]):
            logging.info("Config File changes not Required")
        else:
             logging.debug("HA MasterShip is Changed, Write Process")
             update_ha_proxy_script(dir_ip_address[1])
    elif (ha_status[dir_ip_address[1]] == "SLAVE") and (ha_status[dir_ip_address[0]] == "Null"):
        logging.error ( "HA_STATUS Is Slave in the Director1 and Couldnt Find the Master in another Router.")
        descr_str = verify_debug_status(dir_ip_address[1])
        email_sent("HA Proxy Tool doesnt Have Reachability to the Director0",descr_str)
    elif (ha_status[dir_ip_address[0]] == "SLAVE") and (ha_status[dir_ip_address[1]] == "Null"):
        logging.error ( "HA_STATUS Is Slave in the Director0 and Couldnt Find the Master in another Router.")
        descr_str = verify_debug_status(dir_ip_address[0])
        email_sent("HA Proxy Tool doesnt Have Reachability to the Director1",descr_str)
    else:
        logging.error("Need to Understand the New error state")
