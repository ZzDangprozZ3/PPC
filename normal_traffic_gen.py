import random 
import sysv_ipc



def normal_traffic_gen(key):
    mq = sysv_ipc.MessageQueue(key)
    message = "nouveau traffic"
    type = random.randint(3, 9)
    mq.send(message, type=3)
    print(type)
    
normal_traffic_gen(115)