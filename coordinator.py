from multiprocessing import Process, Array, Value
import os
import sysv_ipc
import time
from lights import handler_east,handler_north,handler_south,handler_west,Lights
from normal_traffic_gen import generate_depart_arrive, one_normal_traffic_gen, normal_traffic_gen, remove_from_queue
from priority_traffic_gen import one_priority_traffic_gen, priority_traffic_gen



def passage_queue_to_queue(queue_depart, queue_destination):   # Move the first traffic in queue depart to the empty place in queue destination
    while 0 not in queue_destination[:]:
        pass
    memory = queue_depart[0]
    remove_from_queue(queue_depart)

    i=0                                            #Place the traffic in to the first free position of queue destination
    while queue_destination[i] != 0:
        i+=1
    queue_destination[i]=memory

def coordinator(key_west, key_south, key_east, key_north):
    PID_Lights = Value('i', 0)             # Create shared memories PID of Lights Process to share with Traffic Generate
    mq_west = sysv_ipc.MessageQueue(key_west, sysv_ipc.IPC_CREAT)    # Create 4 queue 
    mq_south = sysv_ipc.MessageQueue(key_south, sysv_ipc.IPC_CREAT)      
    mq_east = sysv_ipc.MessageQueue(key_east, sysv_ipc.IPC_CREAT)
    mq_north = sysv_ipc.MessageQueue(key_north, sysv_ipc.IPC_CREAT)
    queue_west = Array('i', [0, 0, 0, 0])     # If 0, there is no traffic, if 1, there is an traffic, if 2, its an priority traffic 
    queue_south = Array('i', [0, 0, 0, 0])
    queue_east = Array('i', [0, 0, 0, 0])
    queue_north = Array('i', [0, 0, 0, 0])
    lights_process = Process(target=Lights, args=(handler_west, handler_south, handler_east, handler_north,queue_west,queue_south,queue_east,queue_north,PID_Lights))
    normal_traffic_process = Process(target=normal_traffic_gen, args=(key_west, key_south, key_east, key_north))
    priority_traffic_process = Process(target=priority_traffic_gen, args=(key_west, key_south, key_east, key_north,PID_Lights))
    lights_process.start()
    normal_traffic_process.start()
    priority_traffic_process.start()
    while True:
        if not mq_west.empty():
            message_west, type_west = mq_west.receive()
            update_queue(queue_west,type_west)
        if not mq_south.empty():
            message_south, type_south = mq_south.receive()
        if not mq_east.empty():
            message_east, type_east = mq_east.receive()
        if not mq_north.empty():
            message_north, type_north = mq_north.receive()
        # if (light[0]==1) and (light[2]==1):
        #     message = str(queue_west[0]).encode()
        #     mq.send(message, type=3)
        #     update_queue()
        # elif (light[1]==1) and (light[3]==1):


            
    
        


# if __name__ == "__main__":
#     queue_west= Array('i',[0,0,0,0])
#     queue_south= Array('i',[0,0,0,0])
#     queue_east= Array('i',[0,0,0,0])
#     queue_north= Array('i',[0,0,0,0])
#     childProcess1 = Process(target=lights.Lights, args=(lights.handler_west,lights.handler_south,lights.handler_east,lights.handler_north,queue_west,queue_south,queue_east,queue_north))
#     childProcess2 = Process(target=queues, args=(queue_west,queue_south,queue_east,queue_north))
if __name__ == "__main__":
    print(os.getpid())
    west = Array('i', [1,1,1,1])
    south = Array('i', [1,1,1,1])
    east = Array('i', [1,1,2,1])
    north = Array('i', [1,1,1,1])
    Lights(handler_west,handler_south,handler_east,handler_north,west, south, east, north)
