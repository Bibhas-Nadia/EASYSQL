from colorama import Fore, Style, init
import shutil
import base64
import json

DIR="/opt/easysql/"
#DIR='./'

# Initialize colorama
init(autoreset=True)

# Define the banner text
banner_text = """
     ▄▄▄▄▄▄▄▄     ▄▄       ▄▄▄▄   ▄▄▄    ▄▄▄   ▄▄▄▄      ▄▄▄▄    ▄▄       
     ██▀▀▀▀▀▀    ████    ▄█▀▀▀▀█   ██▄  ▄██  ▄█▀▀▀▀█    ██▀▀██   ██       
     ██          ████    ██▄        ██▄▄██   ██▄       ██    ██  ██       
     ███████    ██  ██    ▀████▄     ▀██▀     ▀████▄   ██    ██  ██       
     ██         ██████        ▀██     ██          ▀██  ██    ██  ██       
     ██▄▄▄▄▄▄  ▄██  ██▄  █▄▄▄▄▄█▀     ██     █▄▄▄▄▄█▀   ██▄▄██▀  ██▄▄▄▄▄▄ 
     ▀▀▀▀▀▀▀▀  ▀▀    ▀▀   ▀▀▀▀▀       ▀▀      ▀▀▀▀▀      ▀▀▀██   ▀▀▀▀▀▀▀▀ 
                                                             ▀           
"""

# Define colors for the banner
colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

# Get the terminal width
terminal_width = shutil.get_terminal_size().columns

# Print the banner at the top center of the terminal
for i, line in enumerate(banner_text.split("\n")):
    if line.strip():  # Skip empty lines
        # Calculate padding to center the line
        padding = (terminal_width - len(line)) // 2
        print(" " * padding + colors[i % len(colors)] + line)

# Reset styles
print(Style.RESET_ALL)



# Function to encode a string in Base64
def encode_base64(data):
    return base64.b64encode(data.encode()).decode()



# Get user inputs
host = input("\tEnter Hostname: ")
user = input("\tEnter Username: ")
database = input("\tEnter Database Name: ")

# Encode all inputs in Base64
credential={}
credential['host'] = encode_base64(host)
credential['user'] = encode_base64(user)
credential['database'] = encode_base64(database)

with open(DIR+"credentials/database_credentials.json",'w') as f:
    f.write(json.dumps(credential))

print("\n\tCredentials are saved sucessfully")