from models import Queue, Process

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

def read_input_file(System, input_filename):
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

def write_output_file(System, output_filename): #in qua trinh xu ly CPU
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