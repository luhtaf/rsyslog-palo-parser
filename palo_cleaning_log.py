import time
log1="FW2-D5"
while True:
    print("Mulai")
    baru=open("/var/log/pa2.log","a")
    cur_line=1
    added=0
    file_line=open("/var/log/cur_line_pa.txt","r")
    line=int(file_line.read())
    file_line.close()
    with open("/var/log/pa.log") as infile:
        for i in infile:
            if cur_line >= line:
                if log1 in i:
                    # print(i.replace("\n",""))
                    baru.write(i)
                    added+=1
                print("Proses, Current Line "+str(cur_line))
            cur_line+=1
    if added>0:
        file_line=open("/var/log/cur_line_pa.txt","w")
        file_line.write(str(cur_line))
        file_line.close()
    # file1.close()
    baru.close()
    print("selesai")
    time.sleep(10)
