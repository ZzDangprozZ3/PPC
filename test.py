import time
from multiprocessing import Array

def remove_from_queue(queue):  # Remove the first traffic in queue
    for i in range(len(queue[:])-1):  # Take away the first traffic in queue, then move the second traffic to first position, do the same with third and fourth traffic
        queue[i]=queue[i+1]
    queue[-1] = 0    #The last position is now free

def starts_with_zeros(queue):    
    i = 0
    while i < len(queue[:]) and queue[i] == 0:
        i += 1
    
    return i > 0 and i < len(queue[:])

def move_forward(queue):
    for i in range(len(queue[:])-1):
        queue[i]= queue[i+1]
    queue[-1]=0

def circulation(queue_west_in, queue_west_out):
    while True:
        print(f"đi vào:{queue_west_in[:]}")
        print(f"đi ra:{queue_west_out[:]}")    
        time.sleep(3)
        if starts_with_zeros(queue_west_in):
            move_forward(queue_west_in)
        if starts_with_zeros(queue_west_out):
            move_forward(queue_west_out)
        else: 
            remove_from_queue(queue_west_out)

a = Array('i',[0,1,0,1,2])
b= Array('i',[0,1,1,0,2])

circulation(a,b)