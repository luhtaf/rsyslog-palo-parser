import socket,re, os

def load_yaml(path):
    import yaml
    with open(path, 'r') as file:
        data = yaml.safe_load(file)
    return data


data=load_yaml('rsyslog_palo.yaml')

# Create a UDP socket to listen on port 514
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", data['rsyslog']['port']))

log_folder=data['log']['path']
# Continuously listen for incoming syslog messages
print("Starting and listen on port 514")
with open( os.path.join(log_folder,data['log']['file']), 'a') as f:
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode("utf-8")

        # Check if message is from PA-VM and contains "THREAT" keyword
        #print(message)
        if f"{data['rsyslog']['name']}" in message:
            log_message = re.sub(r'^<\d+>', '', message)
            f.write(f"{log_message}\n")
            # print(log_message)
