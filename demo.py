from collections import deque
class Process:
    def __init__(self, id, arrival, burst):
        self.id = id # thu tu P1,P2,..
        self.arrival = arrival # thoi gian toi
        self.burst = burst # thoi gian dung cpu
        self.remaining_time = burst  
        self.finish_time = 0
        self.waiting_time = 0

    def get_id(self):
        return self.id
    
    def get_arrival(self):
        return self.arrival
    
    
    def get_burst(self):
        return self.burst

class Queue:
    def __init__(self, id, time_slice, algorithm_type):
        self.id = id # thu tu Q1,Q2,...
        self.time_slice = time_slice # thoi gian cua 1 hang doi
        self.algorithm_type = algorithm_type 
        self.processes = deque()
    
    def add_process(self, process):
        self.processes.append(process)
    
    def get_id(self):
        return self.id
    
    def get_time_slice(self):
        return self.time_slice
    
    def get_algorithm_type(self):
        return self.algorithm_type

    def finish_queue_SJF(self):
        for p in self.processes:
            if p.remaining_time > 0:
                return False        
        return True

    def SJF(self,queue,t):
        if self.finish_queue_SJF():
            return None
        available_processes = []
        for p in queue.processes:
            if p.get_arrival() <= t and p.remaining_time > 0:
                available_processes.append(p)
        if not available_processes:
            return None
        sorted_processes = sorted(available_processes, key=lambda p: (p.remaining_time))
        return sorted_processes[0]

class Sys:
    def __init__(self):
        self.number_of_queue = None
        self.queues = []
        self.RQ = deque() # ready queue
        self.CPU = [None] #thu tu xu ly cpu P1,P2,..., idle

    def add_queue(self, queue):
        if len(self.queues) < self.number_of_queue:
            self.queues.append(queue)
            return True
        return False
    
    def set_number_of_queue(self, number_of_queue):
        self.number_of_queue = number_of_queue

    def all_done(self):
        for q in self.queues:
                for p in q.processes:
                    if p.remaining_time > 0:
                        return False         
        return True
    
    def printCPU(self): #in qua trinh xu ly CPU
        i = 0
        for p in self.CPU:
            print(i, end=":")
            print( p,end=" ")
            i+=1

    def RoundRobin(self):
        t = 0
        if self.all_done():
            return
        
        while not self.all_done():
            check_idle = True

            for cur_queue in self.queues:
                cur_process = None
                temp=[]
                runtime=0
                while runtime<cur_queue.time_slice:
                    if cur_process is None or cur_process.remaining_time == 0:
                        cur_process = cur_queue.SJF(cur_queue, t)
                    
                    if cur_process is None: 
                        break

                    check_idle = False
                    temp.append(f"P{cur_process.get_id()}")
                    cur_process.remaining_time -=1
                    t+=1
                    runtime+=1

                    if cur_process.remaining_time == 0:
                        cur_process.finish_time = t
                    
                self.CPU+=temp
            if check_idle:
                self.CPU.append("idle")
                t+=1

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
        print(f"Queue {queue.get_id()} | Time Slice: {queue.get_time_slice()} | Algorithm: {queue.get_algorithm_type()}")
        for p in queue.processes:
            print(f"  Process {p.get_id()} | Arrival: {p.get_arrival()} | Burst: {p.get_burst()}")
        print()

def main():
    System = Sys()
    input(System)
    test_print(System)
    System.RoundRobin()
    System.printCPU()

main()