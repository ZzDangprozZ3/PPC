from multiprocessing import Process, Array, Value, Lock, Event, Semaphore
import sysv_ipc
import time
import socket
from lights import Lights
from normal_traffic_gen import normal_traffic_gen
from priority_traffic_gen import priority_traffic_gen
from threading import Thread


def key_to_queue(key, queue1, queue2, queue3, queue4):         # Conversion from key to queue
    if key == "1":
        return queue1
    elif key == "2":
        return queue2
    elif key == "3":
        return queue3
    else:
        return queue4

def move_forward(queue):
    for i in range(3):
        if queue[i] == 0:
            queue[i] = queue[i+1]
            queue[i+1] = 0

def circulation(key_west, key_south, key_east, key_north, queue_west_in, queue_west_out, queue_south_in, queue_south_out, queue_east_in, queue_east_out, queue_north_in, queue_north_out, light, lock, change, change_lock, car_lock, create_queue_event, semaphores):
    mq_west = sysv_ipc.MessageQueue(key_west, sysv_ipc.IPC_CREAT)    # Create 4 queue 
    mq_south = sysv_ipc.MessageQueue(key_south, sysv_ipc.IPC_CREAT)      
    mq_east = sysv_ipc.MessageQueue(key_east, sysv_ipc.IPC_CREAT)
    mq_north = sysv_ipc.MessageQueue(key_north, sysv_ipc.IPC_CREAT)
    create_queue_event.set()
    before_move = time.time()
    while True:
        if time.time() - before_move > 3:
            before_move = time.time() 
        # time.sleep(6)   

            with car_lock:
                queue_west_out[0] = 0
                queue_south_out[0] = 0
                queue_east_out[0] = 0
                queue_north_out[0] = 0
                move_forward(queue_west_out)
                move_forward(queue_south_out)
                move_forward(queue_east_out)
                move_forward(queue_north_out)
                with lock:
                    copy_light = light[:]
                if queue_west_in[0] > 0 and copy_light[0] == 1:
                    go_to, t = mq_west.receive()
                    print(f"xe west se di vao huong: {go_to.decode()}")
                    destination = key_to_queue(go_to.decode(),queue_west_out,queue_south_out,queue_east_out,queue_north_out)
                    destination[-1] = queue_west_in[0]
                    queue_west_in[0] = 0
                    semaphores[0].release()
                move_forward(queue_west_in)

                if queue_south_in[0] > 0 and copy_light[1] == 1:
                    go_to, t = mq_south.receive()
                    print(f"xe south se di vao huong: {go_to.decode()}")
                    destination = key_to_queue(go_to.decode(),queue_west_out,queue_south_out,queue_east_out,queue_north_out)
                    destination[-1] = queue_south_in[0]
                    queue_south_in[0] = 0
                    semaphores[1].release()
                move_forward(queue_south_in)

                if queue_east_in[0] > 0 and copy_light[2] == 1:
                    go_to, t = mq_east.receive()
                    print(f"xe east se di vao huong: {go_to.decode()}")
                    destination = key_to_queue(go_to.decode(),queue_west_out,queue_south_out,queue_east_out,queue_north_out)
                    destination[-1] = queue_east_in[0]
                    queue_east_in[0] = 0
                    semaphores[2].release()
                move_forward(queue_east_in)

                if queue_north_in[0] > 0 and copy_light[3] == 1:
                    go_to, t = mq_north.receive()
                    print(f"xe north se di vao huong: {go_to.decode()}")
                    destination = key_to_queue(go_to.decode(),queue_west_out,queue_south_out,queue_east_out,queue_north_out)
                    destination[-1] = queue_north_in[0]
                    queue_north_in[0] = 0
                    semaphores[3].release()
                move_forward(queue_north_in)
            with change_lock:
                change.value = (change.value + 1) % 2

def coordinator_socket(host, port, change, queue_west, queue_west_out, queue_south, queue_south_out, queue_east, queue_east_out, queue_north, queue_north_out, lights, event, car_lock, change_lock):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        event.wait()
        client_socket.connect((host, port))
        current = 1
        while True:
            with change_lock:
                now = change.value
            if current != now:
                current = now
                msg = ""
                with car_lock:
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
                        if lights[i] == 0:
                            msg += "red "
                        else:
                            msg += "green "
                print(msg)

                client_socket.sendall(msg.encode())
            # else: 
            #     client_socket.sendall(("hello").encode())
            #     if len(client_socket.recv(1)) == 0:
            #         break




def coordinator(key_west, key_south, key_east, key_north, host, port, event):
    light = Array('i', [1, 0, 1, 0])    # Red light 1 and green light 0 shared memory
    PID_Lights = Value('i', 0)             # Create shared memories PID of Lights Process to share with Traffic Generate
    change = Value('i', 0)

    #syn
    lock = Lock()
    car_lock = Lock()
    change_lock = Lock()
    getpid_event = Event()
    create_queue_event = Event()
    # circulation_event = Event()
    semaphores = [Semaphore(4) for i in range(4)]

    queue_west = Array('i', [0, 0, 0, 0])     # If 0, there is no traffic, if 1, there is an traffic, if 2, its an priority traffic 
    queue_west_out = Array('i', [0, 0, 0, 0]) 
    queue_south = Array('i', [0, 0, 0, 0])
    queue_south_out = Array('i', [0, 0, 0, 0])
    queue_east = Array('i', [0, 0, 0, 0])
    queue_east_out = Array('i', [0, 0, 0, 0])
    queue_north = Array('i', [0, 0, 0, 0])
    queue_north_out = Array('i', [0, 0, 0, 0])
    lights_process = Process(target=Lights, args=(queue_west, queue_south, queue_east, queue_north, PID_Lights, light, lock, change, change_lock, getpid_event))
    normal_traffic_process = Process(target=normal_traffic_gen, args=(key_west, key_south, key_east, key_north, queue_west, queue_south, queue_east, queue_north, create_queue_event, change, change_lock, car_lock, semaphores))
    priority_traffic_process = Process(target=priority_traffic_gen, args=(key_west, key_south, key_east, key_north, queue_west, queue_south, queue_east, queue_north, PID_Lights, getpid_event, create_queue_event, change, change_lock, car_lock, semaphores))
    circulation_process = Thread(target=circulation, args=(key_west, key_south, key_east, key_north, queue_west, queue_west_out, queue_south, queue_south_out, queue_east, queue_east_out, queue_north, queue_north_out, light, lock, change, change_lock, car_lock, create_queue_event, semaphores))
    socket_thread = Thread(target=coordinator_socket, args=(host, port, change, queue_west, queue_west_out, queue_south, queue_south_out, queue_east, queue_east_out, queue_north, queue_north_out, light, event, car_lock, change_lock))
    lights_process.start()
    normal_traffic_process.start()
    priority_traffic_process.start()
    circulation_process.start()
    socket_thread.start()
    # while True:
    #     print(light[:])
    #     print(f"queue_west : {queue_west[:]}")       
    #     print(f"queue_south : {queue_west[:]}")
    #     print(f"queue_east : {queue_east[:]}")
    #     print(f"queue_north: {queue_north[:]}")
    #     print(f"queue_west_out : {queue_east_out[:]}")
    #     print(f"queue_south_out : {queue_west_out[:]}")
    #     print(f"queue_east_out : {queue_east_out[:]}")
    #     print(f"queue_north_out: {queue_north_out[:]}")
            # change.value = (change.value + 1) % 2

    lights_process.join()
    normal_traffic_process.join()
    priority_traffic_process.join()
    circulation_process.join()
    socket_thread.join()
            
    
        
if __name__ == "__main__":
    coordinator(1,2,3,4)
