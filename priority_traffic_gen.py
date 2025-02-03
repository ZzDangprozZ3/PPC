import sysv_ipc
import os
import signal 
import time
from normal_traffic_gen import generate_depart_arrive,add_to_queue
import random

def priority_traffic_gen(key1,key2,key3,key4, queue_west, queue_south, queue_east, queue_north, PID_Lights): # Generate an priority traffic, arguments are an list has depart and arrive queue's key and PID of process Lights
    while True:    
        frequence = random.randint(10,15) * 3
        time.sleep(frequence)
        direction = generate_depart_arrive(key1,key2,key3,key4)
        if direction[0] == key1: #Update queue
            if queue_west[-1]:
                continue          #If there is no place available in queue, cancel the function, wait for another periode until the queue is available
            os.kill(PID_Lights.value, signal.SIGUSR1)    # Notify to Lights there is an priority traffic coming in West, South, East, North (SIGUSR1,2,RTMIN,RTMAX)
            add_to_queue(queue_west, 2)
        elif direction[0] == key2:
            if queue_south[-1]:
                continue
            os.kill(PID_Lights.value, signal.SIGUSR2) 
            add_to_queue(queue_south, 2)
        elif direction[0] == key3:
            if queue_east[-1]:
                continue
            os.kill(PID_Lights.value, signal.SIGRTMIN)
            add_to_queue(queue_east, 2)
        elif direction[0] == key4:
            if queue_north[-1]:
                continue
            os.kill(PID_Lights.value, signal.SIGRTMAX)
            add_to_queue(queue_north, 2)
        mq = sysv_ipc.MessageQueue(direction[0])
        message = str(direction[1]).encode()  
        mq.send(message,type=2)
        
