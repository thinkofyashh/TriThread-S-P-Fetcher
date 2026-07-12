import threading


counter=0

lock = threading .Lock()
def increment():
    global counter
    for i in range(10**6):
        with lock:
            counter=counter+1

        

thread=[]
for i in range(0,4):
    t=threading.Thread(target=increment)
    thread.append(t)

for i in thread:
    i.start()

for i in thread:
    i.join()


print(counter)    

