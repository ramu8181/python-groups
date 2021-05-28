import keyring
import configparser

config = configparser.ConfigParser()
config.read("haproxy_generator_config.conf")
director_count = config.getint('VERSA_DIRECTOR', 'director_count')
sudo_user = str(config.get("PROXY-SERVER", 'sudopassword'))
print (" Registry of the HaProxy SudoUser Password: ")
passproxy= str(input("Enter the Password of the Haproxy server:  "))
keyring.set_password("PROXY-SERVER",sudo_user, passproxy)

email_user = str(config.get("EMAIL-DETAILS", 'user'))
print (" Registry of the HaProxy Auto Email User Password: ")
emailpassword= str(input("Enter the Password of the Email User:  "))
keyring.set_password("EMAIL-DETAILS",email_user, emailpassword)

director_list = ['VERSA-DIR-{}'.format(i) for i in range(1, director_count + 1)]
for dir_name in director_list:
   username = str(config.get(dir_name, 'username'))
   print (" Registry of the Versa Director Password " + dir_name + ": ")
   passdirect= str(input("Enter the Password of the Director1:  "))
   keyring.set_password(dir_name, username, passdirect)
