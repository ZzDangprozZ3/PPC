import display
import coordinator
import lights
import normal_traffic_gen
import priority_traffic_gen
from multiprocessing import Process, Lock
import time



KEYWEST = 1
KEYSOUTH = 2
KEYEAST = 3
KEYNORTH = 4
HOST = "localhost"
PORT = 3000
WIDTH = 500
HEIGTH = 500
BACKGROUND = "lightblue"


#######
# Main

## Processes
coordinator_p = Process(target=coordinator.coordinator, args=(KEYWEST, KEYSOUTH, KEYEAST, KEYNORTH, HOST, PORT))
display_p = Process(target=display.display, args=(WIDTH, HEIGTH, BACKGROUND, HOST, PORT))
display_p.start()
time.sleep(3)
coordinator_p.start()
coordinator_p.join()
display_p.join()