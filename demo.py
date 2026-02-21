import sys

class Process:
    def __init__(self, id, arrival, burst, id_parent):
        self.id = id # thu tu P1,P2,..
        self.arrival = arrival # thoi gian toi
        self.burst = burst # thoi gian dung cpu
        self.remaining_time = burst  
        self.finish_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.id_parent = id_parent

    def get_id(self):
        return self.id
    
    def get_arrival(self):
        return self.arrival
    
    def get_burst(self):
        return self.burst
    
    def get_id_parent(self):
        return self.id_parent
    
    def get_finish_time(self):
        return self.finish_time
    
    def get_turnaround_time(self):
        return self.turnaround_time
    
    def get_waiting_time(self):
        return self.waiting_time

class Queue:
    def __init__(self, id, time_slice, algorithm_type):
        self.id = id # thu tu Q1,Q2,...
        self.time_slice = time_slice # thoi gian cua 1 hang doi
        self.algorithm_type = algorithm_type 
        self.processes = []
    
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

    def SJF(self,queue,t): # ko phải là SJF, trả về process cần xử lý
        if self.finish_queue_SJF():
            return None
        available_processes = []
        for p in queue.processes:
            if p.get_arrival() <= t and p.remaining_time > 0:
                available_processes.append(p)
        if not available_processes:
            return None
        sorted_processes = sorted(available_processes, key=lambda p: (p.remaining_time, p.get_arrival(), p.get_id()))
        return sorted_processes[0]

class Sys:
    def __init__(self):
        self.number_of_queue = None
        self.queues = []
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

    def calculate_time(self): # tính turnaround và waiting time
        for q in self.queues:
            for p in q.processes:
                p.turnaround_time = p.finish_time - p.arrival
                p.waiting_time = p.turnaround_time - p.burst
        return
    
    def Run(self): #Là Round Robin nhưng để Run cho đẹp
        t = 0
        if self.all_done():
            return
        
        while not self.all_done():
            check_idle = True

            for cur_queue in self.queues:
                cur_process = None
                temp=[]
                runtime=0
                algo = cur_queue.get_algorithm_type() # Lấy tên thuật toán của Queue hiện tại
                while runtime<cur_queue.time_slice:
                    if algo == "SJF":
                        if cur_process is None or cur_process.remaining_time == 0:
                            cur_process = cur_queue.SJF(cur_queue, t)                            
                    elif algo == "SRTN":
                        cur_process = cur_queue.SJF(cur_queue, t)
                    
                    if cur_process is None: 
                        break

                    check_idle = False
                    temp.append(cur_process)
                    cur_process.remaining_time -=1
                    t+=1
                    runtime+=1

                    if cur_process.remaining_time == 0:
                        cur_process.finish_time = t
                    
                self.CPU+=temp
            if check_idle:
                self.CPU.append("idle")
                t+=1
        
        # Kiểm tra xem có vào trường hợp bình thường: Có process chạy
        if len(self.CPU) > 1:
            self.CPU[0] = self.CPU[1]
        else:
            self.CPU.pop(0)   # Trường hợp tệ nhất: Không có process nào chạy cả
        


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

def input(System, input_filename):
    with open(input_filename, "r") as f:
        System.set_number_of_queue(read_number(f))
        is_queues_sorted = False
        while True:
            ch = f.read(1)
            if (ch == "Q"): # id, time_slice, alrogithm_type
                id = read_number(f)
                time_slice = read_number(f)
                alrogithm_type = read_string(f)
                temp = Queue(id, time_slice, alrogithm_type)
                System.add_queue(temp)
            elif(ch == "P"): # id, arrival, burst
                if not is_queues_sorted:
                    System.queues.sort(key=lambda q: q.get_id())
                    is_queues_sorted = True
                
                id = read_number(f)
                arrival = read_number(f)
                burst = read_number(f)
                f.read(1)
                id_parent = read_number(f)
                temp = Process(id, arrival, burst, id_parent)
                for q in System.queues:
                    if (q.get_id() == id_parent):
                        q.add_process(temp)
                        break
            elif(ch == ""):
                if not is_queues_sorted:
                    System.queues.sort(key=lambda q: q.get_id())
                    is_queues_sorted = True
                
                for q in System.queues:
                    q.processes.sort(key = lambda p: p.get_id())

                break

def output(System, output_filename): #in qua trinh xu ly CPU
    with open(output_filename, "w") as f:
        f.write("================== CPU SCHEDULING DIAGRAM ==================\n")
        f.write(f"\n{'[Start - End]':<15} {'Queue':<7} {'Process':<7}\n")
        f.write("----------------------------------\n")
        tmp = System.CPU[0]
        startPoint = 0 # giay bat dat
        for i in range(1,len(System.CPU)):
            endPoint = i-1 # giay ket thuc
            if (System.CPU[i] != tmp):                
                if (tmp != "idle"):
                    f.write(f"{'[' + str(startPoint) + ' - ' + str(endPoint) + ']':<15}")
                    f.write(f" {'Q' + str(tmp.get_id_parent()):<7} ")
                    f.write(f"{'P' + str(tmp.get_id()):<7}\n")
                else:
                    f.write(f"{'[' + str(startPoint) + ' - ' + str(endPoint) + ']':<15} {'':<7} {'Idle':<7}\n")
                startPoint = endPoint
                tmp = System.CPU[i]
        
        if (tmp != "idle"): # xử lý phần tử cuối để in, tại vì nó ko dò đc sự khác biệt để vòng for in rồi
            f.write(f"{'[' + str(startPoint) + ' - ' + str(len(System.CPU)-1) + ']':<15}")
            f.write(f" {'Q' + str(tmp.get_id_parent()):<7} ")
            f.write(f"{'P' + str(tmp.get_id()):<7}\n")
        else:
            f.write(f"{'[' + str(startPoint) + ' - ' + str(len(System.CPU)-1) + ']':<15} {'':<7} {'Idle':<7}\n")

        f.write("\n================ PROCESS STATISTICS ================\n")
        f.write(f"\n{'Process':<12}{'Arrival':<12}{'Burst':<12}{'Completion':<12}{'Turnaround':<12}{'Waiting':<12}\n")
        f.write("----------------------------------------------------------------------\n")
        k = 0
        Avg_turnaround_time = 0
        Avg_waiting_time = 0
        for q in System.queues:
            for p in q.processes:
                f.write(f"{'P' + str(p.get_id()):<12}{p.get_arrival():<12}{p.get_burst():<12}{p.get_finish_time():<12}")
                f.write(f"{p.get_turnaround_time():<12}{p.get_waiting_time():<12}\n")
                Avg_turnaround_time+=p.get_turnaround_time()
                Avg_waiting_time+=p.get_waiting_time()
                k+=1
        
        f.write("----------------------------------------------------------------------\n")
        f.write(f"Average Turnaround Time : {Avg_turnaround_time/k}\n")
        f.write(f"Average Waiting Time : {Avg_waiting_time/k}\n")
        f.write("==================================================")


def test_print(System): # hàm test này đc viết bởi AI, dùng để test đảm bảo input
    print(f"Number of queues: {System.number_of_queue}")
    print()
    for queue in System.queues:
        print(f"Queue {queue.get_id()} | Time Slice: {queue.get_time_slice()} | Algorithm: {queue.get_algorithm_type()}")
        for p in queue.processes:
            print(f"  Process {p.get_id()} | Arrival: {p.get_arrival()} | Burst: {p.get_burst()}")
        print()

def main():
    if len(sys.argv) >= 3:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    else:
        input_filename = "Input.txt"
        output_filename = "Output.txt"
    
    System = Sys()
    input(System, input_filename)
    System.Run()
    System.calculate_time()
    output(System, output_filename)

main()