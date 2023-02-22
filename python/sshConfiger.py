
# This script has to modes: client and server.
# - Client: it will create public and private keys and send them to the server
#   in order to be able to connect to it without entering a password.
# - Server: it will disable password authentication and connecting as root
#   user. Also, it will add rules to the firewall, so that only specific host
#   can connect via SSH and all the others are being denied.

import os
import sys
import subprocess

if(len(sys.argv) == 2 and sys.argv[1] == "client"):
    ssh_dir = os.path.expanduser('~/.ssh')

    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir)

    server_ip = input('Server IP address: ')
    server_user = input('Username for connection: ')

    key_size = '4096'
    key_comment = f'{server_user}@{server_ip}'

    subprocess.run(['ssh-keygen', '-b', key_size, '-C', key_comment])

    privkey_file = os.path.join(ssh_dir, 'id_rsa')

    subprocess.run(['chmod', '600', privkey_file])

    pubkey_file = os.path.join(ssh_dir, 'id_rsa.pub')

    try:
        subprocess.run(['scp', pubkey_file, f'{server_user}@{server_ip}:/home/{server_user}/.ssh/authorized_keys'], check=True)
        print("Success!")
    except subprocess.CalledProcessError as e:
        print('Failed to transfer public key to the server.')
    except KeyboardInterrupt:
        print('Stopped.')
elif(len(sys.argv) == 2 and sys.argv[1] == "server"):

    is_ufw_installed = subprocess.run(['which', 'ufw'], stdout=subprocess.PIPE)
    if is_ufw_installed.returncode != 0:
        print('Fail! ufw is not installed.')
    else:
        client_ip = input("Client IP address: ")
        subprocess.run(['sudo', 'ufw', 'allow', 'from', client_ip, 'to', 'any', 'port', 'ssh'])
        subprocess.run(['sudo', 'ufw', 'deny', 'from', 'any', 'to', 'any', 'port', 'ssh'])
        print("ufw modified successfully!")

        input("Run the script on your client maschine. When it's done, press ENTER.")

        sshd_config_file = '/etc/ssh/sshd_config'

        subprocess.run(['sudo', 'sed', '-i', 's/#PermitRootLogin prohibit-password/PermitRootLogin no/', sshd_config_file])
        subprocess.run(['sudo', 'sed', '-i', 's/#PasswordAuthentication yes/PasswordAuthentication no/', sshd_config_file])
        subprocess.run(['sudo', 'systemctl', 'restart', 'ssh'])
        print("sshd_config modified successfully!")
else:
    print(f"Usage: python(3) {sys.argv[0]} client/server")
