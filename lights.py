import signal
import os
from multiprocessing import Array
import time
from functools import partial  # Help to add an argument to handler



def handler_west(sig, frame, queue_west, light, lock, change, change_lock):
    print("Received SIGUSR1!")
    with lock:
        memory = Array('i', light[:])   # Remember the light's situation before priority traffic's light change
        light[:] = [1,0,0,0]
    with change_lock:
        change.value = (change.value + 1) % 2
    while 2 in queue_west:  
        time.sleep(1)
    with lock:
        light[:] = memory[:]
    with change_lock:
        change.value = (change.value + 1) % 2          # Return the light's situation from beginning
        

def handler_south(sig, frame, queue_south, light, lock, change, change_lock): 
    print("Received SIGUSR2!") 
    with lock:
        memory = Array('i', light[:])                    
        light[:] = [0,1,0,0]
    with change_lock:
        change.value = (change.value + 1) % 2
    while 2 in queue_south:  
        
        time.sleep(1)
    with lock:
        light[:] = memory[:]
    with change_lock:
        change.value = (change.value + 1) % 2

def handler_east(sig, frame, queue_east, light, lock, change, change_lock):
    print("Received SIGRTMIN!")     
    with lock:
        memory = Array('i', light[:])                   
        light[:] = [0,0,1,0]
    with change_lock:
        change.value = (change.value + 1) % 2
    while 2 in queue_east:  
        time.sleep(1)
    with lock:
        light[:] = memory[:]
    with change_lock:
        change.value = (change.value + 1) % 2

def handler_north(sig, frame, queue_north, light, lock, change, change_lock):  
    print("Received SIGRTMAX!")  
    with lock:
        memory = Array('i', light[:])                   
        light[:] = [0,0,0,1]
    with change_lock:
        change.value = (change.value + 1) % 2
    while 2 in queue_north:  
        time.sleep(1)
    with lock:
        light[:] = memory[:]
    with change_lock:
        change.value = (change.value + 1) % 2
    

    
def Lights(queue_west, queue_south, queue_east, queue_north, PID_Lights, light, lock, change, change_lock, getpid_event): 
    signal.signal(signal.SIGUSR1, partial(handler_west, queue_west = queue_west, light = light, lock = lock, change = change, change_lock = change_lock))   # React when we have an priority traffic in any queue 
    signal.signal(signal.SIGUSR2, partial(handler_south, queue_south = queue_south, light = light, lock = lock, change = change, change_lock = change_lock))  
    signal.signal(signal.SIGRTMIN, partial(handler_east, queue_east = queue_east, light = light, lock = lock, change = change, change_lock = change_lock))
    signal.signal(signal.SIGRTMAX, partial(handler_north, queue_north = queue_north, light = light, lock = lock, change = change, change_lock = change_lock))
    PID_Lights.value = os.getpid()
    getpid_event.set()
    before = time.time()
    while True:  # The light change for each 3 seconds    
        if time.time() - before > 12:
            before = time.time()
            with lock:
                for i in range(4):
                    light[i] = (light[i] + 1) % 2
            with change_lock:
                change.value = (change.value + 1) % 2



if __name__ == "__main__":
    print(os.getpid())
    west = Array('i', [1,1,1,1])
    south = Array('i', [1,1,1,1])
    east = Array('i', [1,1,2,1])
    north = Array('i', [1,1,1,1])
    Lights(handler_west,handler_south,handler_east,handler_north,west, south, east, north)  #Work
    