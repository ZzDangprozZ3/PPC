import sysv_ipc
import os
import signal 
import time
from normal_traffic_gen import generate_depart_arrive
import random

def priority_traffic_gen(key1, key2, key3, key4, queue_west, queue_south, queue_east, queue_north, PID_Lights, getpid_event, create_queue_event, change, change_lock, car_lock, semaphores): # Generate an priority traffic, arguments are an list has depart and arrive queue's key and PID of process Lights
    getpid_event.wait()
    create_queue_event.wait()
    periode = random.randint(10,15) * 6
    before = time.time()
    while True:   
        if time.time() - before > periode:
            before = time.time()
            periode = random.randint(10,15) * 6
            # time.sleep(periode)
            direction = generate_depart_arrive(key1,key2,key3,key4)
            if direction[0] == key1: #Update queue
                # if queue_west[-1]:
                #     continue          #If there is no place available in queue, cancel the function, wait for another periode until the queue is available
                semaphores[0].acquire()
                with car_lock:
                    queue_west[-1] = 2
                os.kill(PID_Lights.value, signal.SIGUSR1)    # Notify to Lights there is an priority traffic coming in West, South, East, North (SIGUSR1,2,RTMIN,RTMAX)
            elif direction[0] == key2:
                # if queue_south[-1]:
                #     continue
                semaphores[1].acquire()
                with car_lock:
                    queue_south[-1] = 2
                os.kill(PID_Lights.value, signal.SIGUSR2) 
            elif direction[0] == key3:
                # if queue_east[-1]:
                #     continue
                semaphores[2].acquire()
                with car_lock:
                    queue_east[-1] = 2
                os.kill(PID_Lights.value, signal.SIGRTMIN)
            elif direction[0] == key4:
                # if queue_north[-1]:
                #     continue
                semaphores[3].acquire()
                with car_lock:
                    queue_north[-1] = 2
                os.kill(PID_Lights.value, signal.SIGRTMAX)
            with change_lock:
                change.value = (change.value + 1) % 2
            mq = sysv_ipc.MessageQueue(direction[0])
            message = str(direction[1]).encode()  
            mq.send(message,type=2)
            
