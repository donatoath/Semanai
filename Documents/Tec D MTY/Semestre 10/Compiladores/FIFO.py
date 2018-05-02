import Queue

que = Queue.Queue()

for i in range(5):
    que.put(i)

while not que.empty():
    print que.get()
