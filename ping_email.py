import os
import time
import gmail
from datetime import datetime

report_file = "/home/pi/python_ping/report"
host_goog = "8.8.8.8"
host_cloud = "8.8.4.4"
host_rout = "192.168.1.1"

outage_time = 0
e_outage_time = 0
need_to_send = False
sleep_time = 10
outage_duration = 30

now = datetime.now()
cur_time = now.strftime("%Y%m%d %H%M%S")
with open(report_file, "a") as out_file: out_file.write(cur_time + ": Program Started\n")

while 1:
    now = datetime.now()
    e_now = int(time.time())
    cur_time = now.strftime("%Y%m%d %H%M%S")

    response_goog = os.system("ping -c 1 " + host_goog + ">/dev/null")
    response_cloud = os.system("ping -c 1 " + host_cloud + ">/dev/null")
    response_local = os.system("ping -c 1 " + host_rout + ">/dev/null")

    #if response_goog == 0 and response_cloud == 0 and response_pi1 == 0: 
    #    with open(report_file, "a") as out_file: out_file.write(cur_time + ": all successful\n")

    if response_goog != 0:
        with open(report_file, "a") as out_file: out_file.write(cur_time + ": no response from " +  host_goog + "\n")
    if response_cloud != 0:
        with open(report_file, "a") as out_file: out_file.write(cur_time + ": no response from " + host_cloud + "\n")
    if response_local != 0:
        with open(report_file, "a") as out_file: out_file.write(cur_time + ": no response from " + host_rout + "\n") 

    if need_to_send and response_local != 0:
        need_to_send = False
        with open(report_file, "a") as out_file: out_file.write(cur_time + ": Local became unreachable after WAN failure. Canceling email.\n")
    elif response_goog != 0 and response_cloud != 0 and response_local == 0 and not need_to_send:
        need_to_send = True
        outage_time = cur_time
        e_outage_time = int(time.time())
        with open(report_file, "a") as out_file: out_file.write(cur_time + ": WAN failure! Waiting for receovery to send email.\n")
    elif response_goog == 0 and response_cloud == 0 and response_local == 0 and need_to_send and e_now < e_outage_time + outage_duration:
        need_to_send = False
        with open(report_file, "a") as out_file: out_file.write(cur_time + ": WAN failed starting at " + outage_time + " but it was shorter than 30 seconds. Didn't send email.\n")
    elif need_to_send:
        if e_now >= e_outage_time + outage_duration:
            try: 
                gmail.send(cur_time + " WAN Failure!", "From " + outage_time + " to " + cur_time + " there was a WAN failure. This is indicated by a ping failure to " + host_goog + " and " + host_cloud + " while the router remained reachable.")
                with open(report_file, "a") as out_file: out_file.write(cur_time + ": email sent\n")
                need_to_send = False        
            except: 
                with open(report_file, "a") as out_file: out_file.write(cur_time + ": [WARN] Email Failed!\n") 

    time.sleep(sleep_time)
