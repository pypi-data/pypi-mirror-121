#########################################################
# Malas (Multi-vendor automation leverage at slouching) #
# Version 1.0 build 210926.0001                         #
#########################################################

### What is 'Malas'? ###
'Malas' is a word from Bahasa Indonesia. The 'Malas' word meaning is 'Lazy' (Too inclined to avoid hard work).

### What Malas really is? ###
Malas is a simple multi-vendor network automation program powered by netmiko for general configuration or retrieve information via SSH parallelly.

### Why Malas though? ###
Malas is an abstraction layer in a wizard-type CLI for simplicity's sake.

### Main features ###
- IPv4 target hosts.
- Supported platforms based on netmiko.
- Verify submitted User's file formats before accepted.
- Performing parallel* connectivity tests before remote executions.
  *Parallel tasks capabilities based on CPU's capabilities.
- Performing parallel* remote configurations or retrieve information.
  *Parallel tasks capabilities based on CPU's capabilities.
- Show remote output results immediately.
- Save remote output results per-remote host (Optional).
- Auto-install missing modules (If uninstalled accidentally).

### WIP ###
- IPv6 target hosts
- Hostname target hosts

### Getting started ###

A. Installation:
   'python -m pip install malas' or 'python3 -m pip install malas'

B. Start the program:
   'python -m malas' or 'python3 -m malas'

C. File formatting:
   1. The device information list file's format is a set of three
      that contains IP address, username (has privilege), and password separated by double colons '::'
      per line in row formats, for example (Ignore the bracket):

      #==== Device Information List.txt ====#
      #10.0.0.2::netadmin::password         #
      #10.0.0.3::netadmin::password         #
      #=====================================#

   2. The configuration file's format is one command per line in row formats, for example (Ignore the bracket):

      #========= Configuration.txt =========#
      #interface GigabitEthernet0/11        #
      #description Guest_Networks           #
      #IP address 192.168.1.1 255.255.255.0 #
      #no shutdown                          #
      #exit                                 #
      #do write                             #
      #=====================================#