class Process:
    def __init__(self, id, arrival, burst):
        self.id = id # thu tu P1,P2,..
        self.arrival = arrival # thoi gian toi
        self.burst = burst # thoi gian dung cpu

    def get_id(self):
        return self.id
    
    def get_arrival(self):
        return self.arrival
    
    def get_burst(self):
        return self.burst

class Queue:
    def __init__(self, id, time_slice, alrogithm_type):
        self.id = id # thu tu Q1,Q2,...
        self.time_slice = time_slice # thoi gian cua 1 hang doi
        self.alrogithm_type = alrogithm_type # SRTN/SJF
        self.processes = []
    
    def add_process(self, process):
        self.processes.append(process)
    
    def get_id(self):
        return self.id
    
    def get_time_slice(self):
        return self.time_slice
    
    def get_alrogithm_type(self):
        return self.alrogithm_type

    def al(self):
        pass

class Sys:
    def __init__(self):
        self.number_of_queue = None
        self.queues = []
        RL = [] # hang doi
        CPU = [] # thu tu task ma cpu xu li

    def add_queue(self, queue):
        if len(self.queues) < self.number_of_queue:
            self.queues.append(queue)
            return True
        return False
    
    def set_number_of_queue(self, number_of_queue):
        self.number_of_queue = number_of_queue

    def RR(self):
        t = 0
        
def read_number(f):
    s = ""
    ch = f.read(1)
    while (ch != '\n' and ch != ' ' and ch != ''):
        s+=ch
        ch = f.read(1)    
    return int(s)
    
def read_string(f):
    s = ""
    ch = f.read(1)
    while (ch != '\n' and ch != ' ' and ch != ''):
        s+=ch
        ch = f.read(1)    
    return s

def input(System):
    with open("Input.txt", "r") as f:
        System.set_number_of_queue(read_number(f))
        while True:
            ch = f.read(1)
            if (ch == "Q"): # id, time_slice, alrogithm_type
                id = read_number(f)
                time_slice = read_number(f)
                alrogithm_type = read_string(f)
                temp = Queue(id, time_slice, alrogithm_type)
                System.add_queue(temp)
            elif(ch == "P"): # id, arrival, burst
                id = read_number(f)
                arrival = read_number(f)
                burst = read_number(f)
                f.read(1)
                q_id = read_number(f)
                temp = Process(id, arrival, burst)
                System.queues[q_id - 1].add_process(temp)
            elif(ch == ""):
                break

def test_print(System): # hàm test này đc viết bởi AI, dùng để test đảm bảo input
    print(f"Number of queues: {System.number_of_queue}")
    print()
    for queue in System.queues:
        print(f"Queue {queue.get_id()} | Time Slice: {queue.get_time_slice()} | Algorithm: {queue.get_alrogithm_type()}")
        for p in queue.processes:
            print(f"  Process {p.get_id()} | Arrival: {p.get_arrival()} | Burst: {p.get_burst()}")
        print()

def main():
    System = Sys()
    input(System)
    test_print(System)

main()