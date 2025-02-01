from multiprocessing import Array

a= Array('i',[2,1,1,2,0])
b= Array('i',[1,1,0,0,0])
def passage_queue_to_queue(queue_depart, queue_destination):   # Move the first traffic in queue depart to the empty place in queue destination
    while 0 not in queue_destination[:]:
        pass
    memory = queue_depart[0]

    for i in range(len(queue_depart[:])-1):  # Take away the first traffic in queue, then move the second traffic to first position, do the same with third and fourth traffic
        queue_depart[i]=queue_depart[i+1]
    queue_depart[-1] = 0    #The last position is now free

    i=0                                            #Place the traffic in to the first free position of queue destination
    while queue_destination[i] != 0:
        i+=1
    queue_destination[i]=memory
passage_queue_to_queue(a,b)
print(a[:])
print(b[:])

def add_to_queue(queue, type):   # Add the traffic to queue depart
    while 0 not in queue[:]:
        pass
    i=0
    while queue[i] != 0:
        i +=1
    queue[i] = type

add_to_queue(a,5)
print(a[:])