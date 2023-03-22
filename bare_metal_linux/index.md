# Bare_metal_linux


## UEFI bios and Linux Server

Installing Linux server on HP Desktop with UEFI feature. Expensive lessson I have learned:

Everytime installation failed after it start to copy files, I have tested all kinds of different ways, and it turn out the problem is UEFI. 

> Updated the the next day: The problem wasn't solved this way, I just installed Ubuntu Desktop, that solved the problem.

```
From BIOS -> Boot Order, you can disable the whole UEFI feature here
```
## Modifications after install
### Change IP address with netplan
When installing the OS, I choosed DHCP. After installed successfully, set it statci like this:
```
$  cat /etc/netplan/00-installer-config.yaml
# This is the network config written by 'subiquity'
n#etwork:
  ethernets:
    eno1:
      dhcp4: no
      addresses:
        - 192.168.0.53/24
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
      routes:
        - to: default
          via: 192.168.0.1
  version: 2
  renderer: networkd
$ sudo netplan apply
```
### Correct your hostname
```bash
sudo hostnamectl set-hostname [NEW_HOSTNAME]
```

### Download public key from github 
```bash
$ curl https://api.github.com/users/decmaxn/keys  | jq -r .[].key | tee .ssh/authorized_keys
```

## Local SSH private key and configuration

```bash
$ eval "$(ssh-agent -s)"
$ ssh-add ~/.ssh/vma_rsa  # the vma_rsa file can't be 755, 600 works.
$ ssh-add -l  # confirm the key is in memory

$ cat ~/.ssh/config
Host 192.168.0.*
  User vma
  IdentityFile ~/.ssh/vma_rsa

Host 51
  Hostname 192.168.0.51
Host 52
  Hostname 192.168.0.52
Host 53
  Hostname 192.168.0.53
Host 54
  Hostname 192.168.0.54

$ ssh 51
```

## Check network speed

```bash
sudo apt-get install curl
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
sudo apt-get install speedtest
```

