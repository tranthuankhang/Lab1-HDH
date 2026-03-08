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

    def finish_queue(self):
        for p in self.processes:
            if p.remaining_time > 0:
                return False        
        return True

    def SJ(self,queue,t): #trả về process cần xử lý
        if self.finish_queue():
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
                            cur_process = cur_queue.SJ(cur_queue, t)                            
                    elif algo == "SRTN":
                        cur_process = cur_queue.SJ(cur_queue, t)
                    
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