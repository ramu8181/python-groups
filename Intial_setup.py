import os
import re
try:
    import configparser
except:
     #install_the_module("keyring")
     print ("Trying to Install required module: configparser\n")
     os.system("python3  -m pip install configparser")

try:
    import keyring
except ImportError:
    #install_the_module("keyring")
    print ("Trying to Install required module: keyring\n")
    os.system('pip install --upgrade pip')
    os.system('python -m pip install keyring')
    print ("Trying to Install required module: keyring.alt\n")
    os.system('python -m pip install  keyrings.alt')

import keyring.backend
import getpass
try:
   import apt
except:
   os.system('pip install --upgrade pip')
   os.system('pip3 install --upgrade pip')
   os.system('python3 -m pip install apt')
try:
   import haproxy_generator
except:
    print ("Trying to Install required module: keyring.alt\n")
    os.system('python3 -m pip install  keyrings.alt')
    os.system('python -m pip install requests')
    print("PIP upgradation Process")
    os.system('pip install --upgrade pip')
    os.system('pip3 install --upgrade pip')
    os.system('python3 -m pip install setuptools_rust')
    os.system('python -m pip install  keyrings.alt')
    os.system('python3 -m pip install netmiko')

import haproxy_generator
import subprocess

def vm_registry(config):
    sudo_user = str(config.get("PROXY-SERVER", 'sudopassword'))
    print (" Registry of the HaProxy SudoUser Password: ")
    passproxy= getpass.getpass("Enter the Password of the Haproxy VM server:  ")
    keyring.set_password("PROXY-SERVER",sudo_user, passproxy)

def email_registry(config):
    email_user = str(config.get("EMAIL-DETAILS", 'user'))
    print (" Registry of the HaProxy Auto Email User Password: ")
    emailpassword= getpass.getpass("Enter the Password of the Email User:  ")
    keyring.set_password("EMAIL-DETAILS",email_user, emailpassword)

def director_registry(config):
    director_count = config.getint('VERSA_DIRECTOR', 'director_count')
    config.read("haproxy_generator_config.conf")
    director_list = ['VERSA-DIR-{}'.format(i) for i in range(1, director_count + 1)]
    for dir_name in director_list:
       username = str(config.get(dir_name, 'username'))
       print (" Registry of the Versa Director Password of  " + dir_name + ": ")
       passdirect= getpass.getpass("Enter the Password of the "  +  dir_name + ":  " )
       keyring.set_password(dir_name, username, passdirect)

def all_call(config):
    vm_registry(config)
    email_registry(config)
    director_registry(config)    

def package_installation():
    pkg_name = "apache2"
    cache = apt.cache.Cache()
    cache.update()
    cache.open()

    pkg = cache[pkg_name]
    if pkg.is_installed:
       print ("{pkg_name} already installed".format(pkg_name=pkg_name))
    else:
       pkg.mark_install()

    try:
        cache.commit()
    except:
        print (" package installation failed [{err}]".format(err=str(arg)))

def basic_rest_api_query(dir1_ip):
    try:
         dir1 = "https://" + dir1_ip + ":9182/api/config/vnmsha/actions/_operations/status"
         post = requests.post(url=dir1, auth=(username, password),
         verify=False, headers={'accept': 'application/json'})
         stat = json.dumps(post.json(), indent=4)
         print (stat)
    except:
         print("Rest API call is not working for fine " + dir1_ip)

if __name__=='__main__':
  status = os. system("dpkg -s python-pip | grep Status")
  config = configparser.ConfigParser()
  config.read("haproxy_generator_config.conf")
  all_call(config)
  print (" Enable the Sanity checks of the Passwords Collected:")
  subject = "Test"
  description = "Test"
  try:
    haproxy_generator.email_sent(subject,description)
    print("Verify Mail Has Successfully Received")
  except:
    print("Email Password is not accepted, Exception raised")
  dir_ip_address = haproxy_generator.population_ha_nodes()
  ha_status = haproxy_generator.rest_api_query(dir_ip_address)
  print (ha_status)
  for key,values in ha_status.items():
      if "Null" in values:
        print ( "Rest API Call for the Director " + key + " is failed")
      else: 
        print ( "Rest API Call for the Director " + key + " is Passed")
  print("Install the apache2 and haproxy with the following commands")
  print ("apt-get install haproxy & apache2")
