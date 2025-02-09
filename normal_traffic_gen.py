import random 
import sysv_ipc
import time




def generate_depart_arrive(key1,key2,key3,key4):  #Return a list which has depart and arrive queue's key
    random_list = [key1,key2,key3,key4]
    res= [random.choice(random_list)]  # Chose an key randomly from randomlist
    random_list.pop(random_list.index(res[0])) # Remove that key from randomlist
    res.append(random.choice(random_list))  # Chose an key from randomlist modified
    return res


def normal_traffic_gen(key1, key2, key3, key4, queue_west, queue_south, queue_east, queue_north, create_queue_event, change, change_lock, car_lock, semaphores): #Generate un traffic, argument is an list has depart and arrive queue's key
    create_queue_event.wait()
    before = time.time()
    periode = random.randint(1, 6) *3
    while True:    
        if time.time() - before > periode:
            before = time.time()
            periode = random.randint(1, 6) * 6
            direction = generate_depart_arrive(key1, key2, key3, key4)
            # print(direction)
            if direction[0] == key1: #Update queue
                # if queue_west[-1]:
                #     continue            #If there is no place available in queue, cancel the function, wait for another periode until the queue is available
                semaphores[0].acquire()
                with car_lock:
                    queue_west[-1] = 1
                print(f"queuewestmodified:{queue_west[:]}")
            elif direction[0] == key2:
                # if queue_south[-1]:
                #     continue
                semaphores[1].acquire()
                with car_lock:
                    queue_south[-1] = 1
                print(f"queuesouthmodified:{queue_south[:]}")
            elif direction[0] == key3:
                # if queue_east[-1]:
                #     continue
                semaphores[2].acquire()
                with car_lock:
                    queue_east[-1] = 1
                print(f"queueeastmodified:{queue_east[:]}")
            elif direction[0] == key4:
                # if queue_north[-1]:
                #     continue
                semaphores[3].acquire()
                with car_lock:
                    queue_north[-1] = 1   
                print(f"queuenorthmodified:{queue_north[:]}")  
            with change_lock:
                change.value = (change.value + 1) % 2
            mq = sysv_ipc.MessageQueue(direction[0])
            go_to = str(direction[1]).encode()  # Envoyer sa key destination comme message
            mq.send(go_to, type=1)
    

# def add_to_queue(queue, type):   # Add the traffic to available spot in queue depart
#     # while 0 not in queue[:]:
#     #     pass
#     queue[-1] = type     # Add the traffic to the last position of queue


# def remove_from_queue(queue):  # Remove the first traffic in queue
#     for i in range(len(queue[:])-1):  # Take away the first traffic in queue, then move the second traffic to first position, do the same with third and fourth traffic
#         queue[i]=queue[i+1]
#     queue[-1] = 0    #The last position is now free


if __name__ == "__main__":
    pass