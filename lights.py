import signal
import os
import sys
from multiprocessing import Process, Array, Value
import time
from functools import partial  # Help to add an argument to handler



def handler_west(sig, frame, queue_west):
    print("Received SIGUSR1!")
    global light
    memory = Array('i', light[:])   # Remember the light's situation before priority traffic's light change
    light[:] = [1,0,0,0]
    print(light[:])
    while 2 in queue_west:  # Wait until priority traffic dissapear
        time.sleep(2)  # Saving CPU from woking 100%
    light[:] = memory[:]            # Return the light's situation from beginning
        

def handler_south(sig, frame, queue_south): 
    print("Received SIGUSR2!")
    global light   
    memory = Array('i', light[:])                    
    light[:] = [0,1,0,0]
    print(light[:])
    while 2 in queue_south:  
        time.sleep(2)
    light[:] = memory[:]

def handler_east(sig, frame, queue_east):
    print("Received SIGRTMIN!")    
    global light   
    memory = Array('i', light[:])                   
    light[:] = [0,0,1,0]
    print(light[:])
    while 2 in queue_east:  
        time.sleep(2)  
    light[:] = memory[:]

def handler_north(sig, frame, queue_north):  
    print("Received SIGRTMAX!") 
    global light   
    memory = Array('i', light[:])                   
    light[:] = [0,0,0,1]
    print(light[:])
    while 2 in queue_north:  
        time.sleep(2)
    light[:] = memory[:]
    print(f"light after change:{light[:]}")

    
def Lights(handler_west,handler_south,handler_east,handler_north, queue_west, queue_south, queue_east, queue_north, PID_Lights): 
    PID_Lights.value = os.getpid()
    global light 
    light = []
    light1 = Array('i', [1,0,1,0]) # Consider that 1 = Green Light and 0 = Red Light. From left to right : West, South, East, North
    light2 = Array('i', [0,1,0,1])
    while True:  # The light change for each 3 seconds
        signal.signal(signal.SIGUSR1, partial(handler_west,queue_west=queue_west))   # React when we have an priority traffic in any queue 
        signal.signal(signal.SIGUSR2, partial(handler_south, queue_south=queue_south))  
        signal.signal(signal.SIGRTMIN, partial(handler_east, queue_east=queue_east))
        signal.signal(signal.SIGRTMAX, partial(handler_north, queue_north=queue_north))
        light = light1
        print(light[:])
        time.sleep(3)
        light = light2
        print(light[:])
        time.sleep(3)     


if __name__ == "__main__":
    print(os.getpid())
    west = Array('i', [1,1,1,1])
    south = Array('i', [1,1,1,1])
    east = Array('i', [1,1,2,1])
    north = Array('i', [1,1,1,1])
    Lights(handler_west,handler_south,handler_east,handler_north,west, south, east, north)  #Work
    