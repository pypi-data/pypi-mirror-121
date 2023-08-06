# amxtelnet
### amx telnet functions

## Telnet():
#### Handles the actual telnet connection and communication with the AMX devices. This class is very universal, but if you run into issues using it on a non-AMX device, it may be caused by the modifications I had to make for AMX:
##### Using the default telnetlib.py with AMX was causing an infinite handshake loop.
##### _write() lines 269, 270 disabled IAC (telnet negotiation) doubling.
##### process_rawq() lines 373, 374 changed when raw chars go to buf when IAC.


## AMXConnect():

### returns:
#### commands are send to AMX masters. If desired, replies are written to file as .txt and/or logged.
### set_systems():
#### list of dicts where each dict is an AMX system.
#### minimum key requirements:
##### 'full_name' (string)
##### 'master_ip' (string)
##### 'master_model' (string) (NX-1200, NI-700, etc.)

### config():
#### user_name: user name to login to AMX
#### password: password to login to AMX
#### alt_username: user name to use if user_name fails
#### alt_password: password to use with alt_user_name
#### write_results: True or False; write replies to individual .txt files per system.
#### output_path: file path to use if write_results is True. This path should also be used for the path in ParseAMXResponse().
#### set_requests(): list of strings to send to the AMX master. $0D is automaticallyv appended.
#### run(): Begin connecting to systems in set_systems(), sending requests from set_requests(), using settings from config()


## ParseAMXResponse():
#### Use this class to parse the information gathered from AMXConnect().
#### This class is less universal in that it expects the .txt files to contain responses to the following commands in the following order:
##### 'show device','get ip','program info','list'
#### You can append additional commands as needed. The output of ParseAMXResponse().read_telnet_text() is a list of amx system dicts. Current uses of this list:

##### export to excel using amxtoexcel.py to archive campus system status

##### code creation using code_creator_django.py or code_creator_usm.py

#### AMXConnect.path and ParseAMXResponse.path will normally refer to the same location. If you use the default locations in each class, they'll work together using systems/telnet responses/.

#### If there's already .txt files in 'path' you can skip AMXConnect() and go straight to ParseAMXResponse() if using potentially outdated information is acceptable.
