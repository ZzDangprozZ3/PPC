import signal
import os
from multiprocessing import Array
import time
from functools import partial  # Help to add an argument to handler



def handler_west(sig, frame, queue_west, light):
    print("Received SIGUSR1!")
    memory = Array('i', light[:])   # Remember the light's situation before priority traffic's light change
    light[:] = [1,0,0,0]
    while 2 in queue_west:  # Wait until priority traffic dissapear
        time.sleep(1)  # Saving CPU from woking 100%
    light[:] = memory[:]            # Return the light's situation from beginning
        

def handler_south(sig, frame, queue_south, light): 
    print("Received SIGUSR2!") 
    memory = Array('i', light[:])                    
    light[:] = [0,1,0,0]
    while 2 in queue_south:  
        time.sleep(1)
    light[:] = memory[:]

def handler_east(sig, frame, queue_east, light):
    print("Received SIGRTMIN!")     
    memory = Array('i', light[:])                   
    light[:] = [0,0,1,0]
    while 2 in queue_east:  
        time.sleep(1)  
    light[:] = memory[:]

def handler_north(sig, frame, queue_north, light):  
    print("Received SIGRTMAX!")  
    memory = Array('i', light[:])                   
    light[:] = [0,0,0,1]
    while 2 in queue_north:  
        time.sleep(1)
    light[:] = memory[:]
    

    
def Lights(handler_west, handler_south, handler_east, handler_north, queue_west, queue_south, queue_east, queue_north, PID_Lights,light): 
    PID_Lights.value = os.getpid()
    signal.signal(signal.SIGUSR1, partial(handler_west,queue_west=queue_west, light= light))   # React when we have an priority traffic in any queue 
    signal.signal(signal.SIGUSR2, partial(handler_south, queue_south=queue_south, light = light))  
    signal.signal(signal.SIGRTMIN, partial(handler_east, queue_east=queue_east, light = light))
    signal.signal(signal.SIGRTMAX, partial(handler_north, queue_north=queue_north, light = light))
    while True:  # The light change for each 3 seconds    
        time.sleep(12)
        for i in range(4):
            light[i] = (light[i] + 1) % 2



if __name__ == "__main__":
    print(os.getpid())
    west = Array('i', [1,1,1,1])
    south = Array('i', [1,1,1,1])
    east = Array('i', [1,1,2,1])
    north = Array('i', [1,1,1,1])
    Lights(handler_west,handler_south,handler_east,handler_north,west, south, east, north)  #Work
    