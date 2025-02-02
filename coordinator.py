from multiprocessing import Process, Array, Value
import os
import sysv_ipc
import time
import socket
from lights import handler_east,handler_north,handler_south,handler_west,Lights
from normal_traffic_gen import normal_traffic_gen, remove_from_queue
from priority_traffic_gen import priority_traffic_gen
from threading import Thread



def passage_queue_to_queue(queue_depart, queue_destination):   # Move the first traffic in queue depart to the empty place in queue destination
    memory = queue_depart[0]
    remove_from_queue(queue_depart)
    queue_destination[-1]=memory

def key_to_queue(key,queue1, queue2, queue3,queue4):         # Conversion from key to queue
    if key ==1:
        return queue1
    elif key == 2:
        return queue2
    elif key == 3:
        return queue3
    else:
        return queue4

def move_forward(queue):
    for i in range(len(queue[:])-1):
        queue[i]= queue[i+1]
    queue[-1]=0

def circulation(key_west,key_south,key_east, key_north, queue_west_in, queue_west_out, queue_south_in, queue_south_out, queue_east_in, queue_east_out, queue_north_in, queue_north_out, light):
    mq_west = sysv_ipc.MessageQueue(key_west)    # Create 4 queue 
    mq_south = sysv_ipc.MessageQueue(key_south)      
    mq_east = sysv_ipc.MessageQueue(key_east)
    mq_north = sysv_ipc.MessageQueue(key_north)
    while True:    
        time.sleep(3)
        if queue_west_in[0]==0:                                  #If there is a space ahead, just go ahead
            move_forward(queue_west_in)
        elif light[0] == 1:                                      # If no space and the light is green, just go to another queue
            go_to, t = mq_west.receive()
            passage_queue_to_queue(queue_west_in, key_to_queue(go_to.decode(),queue_west_out,queue_south_out,queue_east_out,queue_north_out))           
        if queue_west_out[0]==0:
            move_forward(queue_west_out)
        else: 
            remove_from_queue(queue_west_out)


        if queue_south_in[0]==0:
            move_forward(queue_south_in)
        elif light[1] == 1:  
            go_to, t = mq_south.receive()
            passage_queue_to_queue(queue_south_in, key_to_queue(go_to.decode(),queue_west_out,queue_south_out,queue_east_out,queue_north_out))  
        if queue_south_out[0]==0:
            move_forward(queue_south_out)
        else: 
            remove_from_queue(queue_south_out)


        if queue_east_in[0]==0:
            move_forward(queue_east_in)
        elif light[2] == 1:  
            go_to, t = mq_east.receive()
            passage_queue_to_queue(queue_east_in, key_to_queue(go_to.decode(),queue_west_out,queue_south_out,queue_east_out,queue_north_out))  
        if queue_east_out[0]==0:
            move_forward(queue_east_out)
        else: 
            remove_from_queue(queue_east_out)

            
        if queue_north_in[0]==0:
            move_forward(queue_north_in)
        elif light[3] == 1:  
            go_to, t = mq_north.receive()
            passage_queue_to_queue(queue_north_in, key_to_queue(go_to.decode(),queue_west_out,queue_south_out,queue_east_out,queue_north_out))      
        if queue_north_out[0]==0:
            move_forward(queue_north_out)
        else: 
            remove_from_queue(queue_north_out)
    
    

def coordinator_socket(host, port, change, queue_west, queue_west_out, queue_south, queue_south_out, queue_east, queue_east_out, queue_north, queue_north_out, lights):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        current = 1
        while True:
            if current != change.value:
                current = change.value
                msg = ""
                for i in range(4):
                    if queue_north_out[i] == 1:
                        msg += "gray "
                    elif queue_north_out[i] == 2:
                        msg += "red "
                    else:
                        msg += "None "
                #################################
                for i in range(4):
                    if queue_north[3-i] == 1:
                        msg += "gray "
                    elif queue_north[3-i] == 2:
                        msg += "red "
                    else:
                        msg += "None "
                ######################################
                for i in range(4):
                    if queue_south_out[i] == 1:
                        msg += "gray "
                    elif queue_south_out[i] == 2:
                        msg += "red "
                    else:
                        msg += "None "
                #################################
                for i in range(4):
                    if queue_south[3-i] == 1:
                        msg += "gray "
                    elif queue_south[3-i] == 2:
                        msg += "red "
                    else:
                        msg += "None "
                #################################
                for i in range(4):
                    if queue_east_out[i] == 1:
                        msg += "gray "
                    elif queue_east_out[i] == 2:
                        msg += "red "
                    else:
                        msg += "None "
                #################################
                for i in range(4):
                    if queue_east[3-i] == 1:
                        msg += "gray "
                    elif queue_east[3-i] == 2:
                        msg += "red "
                    else:
                        msg += "None "
                ###################################
                for i in range(4):
                    if queue_west_out[i] == 1:
                        msg += "gray "
                    elif queue_west_out[i] == 2:
                        msg += "red "
                    else:
                        msg += "None "
                #################################
                for i in range(4):
                    if queue_west[3-i] == 1:
                        msg += "gray "
                    elif queue_west[3-i] == 2:
                        msg += "red "
                    else:
                        msg += "None "
                ###################################
                for i in range(4):
                    if lights[i] == 1:
                        msg += "red "
                    else:
                        msg += "green "
                print(msg)

                client_socket.sendall(msg.encode())




def coordinator(key_west, key_south, key_east, key_north, host, port):
    light = Array('i',[1,0,1,0])    # Red light 1 and green light 0 shared memory
    PID_Lights = Value('i', 0)             # Create shared memories PID of Lights Process to share with Traffic Generate
    change = Value('i', 0)
    mq_west = sysv_ipc.MessageQueue(key_west, sysv_ipc.IPC_CREAT)    # Create 4 queue 
    mq_south = sysv_ipc.MessageQueue(key_south, sysv_ipc.IPC_CREAT)      
    mq_east = sysv_ipc.MessageQueue(key_east, sysv_ipc.IPC_CREAT)
    mq_north = sysv_ipc.MessageQueue(key_north, sysv_ipc.IPC_CREAT)
    queue_west = Array('i', [0, 0, 0, 0])     # If 0, there is no traffic, if 1, there is an traffic, if 2, its an priority traffic 
    queue_west_out = Array('i', [0, 0, 0, 0]) 
    queue_south = Array('i', [0, 0, 0, 0])
    queue_south_out = Array('i', [0, 0, 0, 0])
    queue_east = Array('i', [0, 0, 0, 0])
    queue_east_out = Array('i', [0, 0, 0, 0])
    queue_north = Array('i', [0, 0, 0, 0])
    queue_north_out = Array('i', [0, 0, 0, 0])
    lights_process = Process(target=Lights, args=(handler_west, handler_south, handler_east, handler_north,queue_west,queue_south,queue_east,queue_north,PID_Lights,light))
    normal_traffic_process = Process(target=normal_traffic_gen, args=(key_west, key_south, key_east, key_north,queue_west,queue_south,queue_east,queue_north))
    priority_traffic_process = Process(target=priority_traffic_gen, args=(key_west, key_south, key_east, key_north,queue_west,queue_south,queue_east,queue_north,PID_Lights))
    circulation_process = Process(target=circulation, args=(key_west, key_south, key_east, key_north,queue_west,queue_west_out,queue_south,queue_south_out,queue_east,queue_east_out,queue_north,queue_north_out,light))
    socket_thread = Thread(target=coordinator_socket, args=(host, port, change, queue_west, queue_west_out, queue_south, queue_south_out, queue_east, queue_east_out, queue_north, queue_north_out, light))
    lights_process.start()
    normal_traffic_process.start()
    priority_traffic_process.start()
    circulation_process.start()
    socket_thread.start()
    while True:
        time.sleep(1)
        print(light[:])
        print(f"queue_west : {queue_west[:]}")       
        print(f"queue_south : {queue_west[:]}")
        print(f"queue_east : {queue_east[:]}")
        print(f"queue_north: {queue_north[:]}")
        print(f"queue_west_out : {queue_east_out[:]}")
        print(f"queue_south_out : {queue_west_out[:]}")
        print(f"queue_east_out : {queue_east_out[:]}")
        print(f"queue_north_out: {queue_north_out[:]}")
        change.value = (change.value + 1) % 2

    lights_process.join()
    normal_traffic_process.join()
    priority_traffic_process.join()
    circulation_process.join()
    socket_thread.join()
            
    
        
if __name__ == "__main__":
    coordinator(1,2,3,4)
