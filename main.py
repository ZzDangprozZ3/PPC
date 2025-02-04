import display
import coordinator
from multiprocessing import Process, Event



KEYWEST = 1
KEYSOUTH = 2
KEYEAST = 3
KEYNORTH = 4
HOST = "localhost"
PORT = 3000
WIDTH = 500
HEIGTH = 500
BACKGROUND = "lightblue"


event = Event() 
#######
# Main

## Processes
coordinator_p = Process(target=coordinator.coordinator, args=(KEYWEST, KEYSOUTH, KEYEAST, KEYNORTH, HOST, PORT, event))
display_p = Process(target=display.display, args=(WIDTH, HEIGTH, BACKGROUND, HOST, PORT, event))
display_p.start()
coordinator_p.start()
display_p.join()
coordinator_p.join()