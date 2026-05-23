# Implement a syslog parse for iptables, retrieve relevant information, format into json output
# 1) Use regex to retrieve relevant information
# 2) Use dictionaries to map captured information to format
# 3) Format each log to be structured json output

# **********************************************************************
# Use these two sources below
# https://www.w3schools.com/python/python_regex.asp
# https://developers.google.com/edu/python/regular-expressions
# **********************************************************************

import json
import re

file_path = 'iptables.log'

with open(file_path, 'r') as file:
    lines = file.readlines() # stores each line as a index in lines array

#pattern = r'IN=(\S*)\s+OUT=(\S*)\s+.*?SRC=(\S*)\s+DST=(\S*)\s+LEN=(\S*)\s+.*?PROTO=(\S*)\s+SPT=(\S*)\s+DPT=(\S*)'
pattern = r'(\w+)=([^\s]*)' 
# (\w+) defines a group of any word character, where it finds one or more occurences
# = just separates the indentifier such as "IN="
# ([^\s]*) defines a group of any non white space character with zero or more occurences
json_output = []

# for line in lines:
#     match = re.search(pattern, line)

#     if match:
#         obj = {
#             "IN": match.group(1),
#             "OUT": match.group(2),
#             "SOURCE_IP": match.group(3),
#             "DESTINATION_IP": match.group(4),
#             "LENGTH": match.group(5),
#             "PROTOCOL": match.group(6),
#             "SOURCE_PORT": match.group(7),
#             "DESTINATION_PORT": match.group(8)
#         }
    
#         json_output.append(obj)

# for all lines in the log file
for line in lines:
    pair = re.findall(pattern, line) # returns a list of all matching patterns
    data = dict(pair) # stores each pair as a dict
    obj = { # choose the output we want
        "IN": data.get("IN", ""),
        "OUT": data.get("OUT", ""),
        "SOURCE_IP": data.get("SRC", ""),
        "DESTINATION_IP": data.get("DST", ""),
        "PROTOCOL": data.get("PROTO", ""),
        "SOURCE_PORT": data.get("SPT", ""),
        "DESTINATION_PORT": data.get("DPT", "")
    }
    json_output.append(obj) # append it to a list

# write it to a json file
write_file = 'iptables.json'
with open(write_file, 'w') as json_file:
    json.dump(json_output, json_file, indent=4)
