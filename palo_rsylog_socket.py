import socket,re, os
from datetime import datetime

def load_yaml(path):
    import yaml
    with open(path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def check_rsyslog_in_message(nama_rsyslog, message):
    index=0
    for string in nama_rsyslog:
        if string in message:
            return True,index
        index=index+1
    return False,0




data=load_yaml('rsyslog_palo.yaml')
files=data['log']['file']
nama_rsyslog=data['rsyslog']['name']

if len(nama_rsyslog)!=len(files):
    print("Config rsyslog_palo.yaml salah, jumlah log.file dan rsyslog.name tidak sama")
    exit(0)

# Create a UDP socket to listen on port 514
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", data['rsyslog']['port']))

log_folder=data['log']['path']
# Continuously listen for incoming syslog messages
print("Starting and listen on port 514")
initial_time=datetime.now().day
f=[]
for file in files:
    f.append(open(os.path.join(log_folder,file), 'a'))
# with open( os.path.join(log_folder,data['log']['file']), 'a') as f:
while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode("utf-8")

    # Check if message is from PA-VM and contains "THREAT" keyword
    #print(message)
    apakah_rsyslog=check_rsyslog_in_message(nama_rsyslog, message)
    if apakah_rsyslog[0]:
        log_message = re.sub(r'^<\d+>', '', message)
        # f.write(f"{log_message}\n")
        f[apakah_rsyslog[1]].write(str(log_message)+"\n")
        print(log_message)
        current_time=datetime.now().day
        if initial_time != current_time:
            index=0
            for file in files:
                f[index].close()                
                f.pop(index)
                f.insert(index,open(os.path.join(log_folder, file), 'a'))              
                initial_time=datetime.now()
                index=index+1

