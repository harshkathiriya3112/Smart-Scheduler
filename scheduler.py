from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import copy
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.interactive(True)


def browse_input():
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
    
    # go update list
    if(filename==''):
        filename='This path is not working.'
    else:
        i = 0
        data.clear()
        file = open(filename, "r")
        for line in file:
            endl = line.find('\n')
            if endl != -1 :
                line = line[:endl]
            if i == 0:
                pnum = line
            else:
                line = line.split(' ')
                # Process No.  ( Arriv , Runing , Priority )
                data[int(line[0])] = [float(line[1]),float(line[2]),float(line[3])]
            i+=1
        file.close()
        
    path_label.config(text=filename)
    update_graph()
    return




def DO_FCFS():
    output.clear()
    X_time.clear()
    Y_prun.clear()
    CSTime = context_val.get()
    sorted_data = sorted(data.items(), key=lambda kv: kv[1])
    # Process No.  ( Arriv , Runing , Priority )
    AccumTime = 0
    prevX = 0
    prevY = 0
    for p in sorted_data:
        # P.Arriv
        pno = int(p[0])
        arrival = float(p[1][0])
        burst = float(p[1][1])
        
        if (arrival > prevX):
            X_time.append(prevX)
            Y_prun.append(0)
            X_time.append(arrival)
            Y_prun.append(0)
            X_time.append(arrival)
            Y_prun.append(pno)
            X_time.append(burst+arrival)          
            Y_prun.append(pno)
            #X_time.append(burst+arrival)          
            #Y_prun.append(0)
            prevX = arrival+burst
        else:
            X_time.append(prevX)
            Y_prun.append(pno)
            X_time.append(prevX+burst)          
            Y_prun.append(pno)
            prevX = prevX+burst
            
        output[pno] = [pno,arrival,burst,prevX,(prevX-arrival-burst),(prevX-arrival),(prevX-arrival)/burst]
        
    X_time.append(prevX)
    Y_prun.append(0)
    return



    
def DO_HPF():
    output.clear()
    X_time.clear()
    Y_prun.clear()
    CSTime = context_val.get()
    # Sorting with respect to Arrival Time
    sorted_data = sorted(data.items(), key=lambda kv: kv[1][0])
    pnum = (len(sorted_data))    
    # Process No.  ( Arriv , Runing , Priority )
    AccumTime = (sorted_data[0][1][0])
    prevX = 0
    prevY = 0
    j = 0
    i = 0
    Queue = {}

    for i in range (pnum):
        Queue = dict(Queue)
        while (j < pnum and sorted_data[j][1][0] <= AccumTime ):
            Queue[(sorted_data[j][0])] = sorted_data[j][1]
            j +=1
        Queue = sorted(Queue.items(), key=lambda kv: kv[1][2],reverse=True)
        if (len(Queue) == 0):
            p = sorted_data[i]
        else:
            p =  Queue.pop(0)
        pno = p[0]
        arrival = p[1][0]
        burst = p[1][1]
        if (arrival > prevX):
            X_time.append(prevX)
            Y_prun.append(0)
            X_time.append(arrival)
            Y_prun.append(0)
            X_time.append(arrival)
            Y_prun.append(pno)
            X_time.append(burst+arrival)          
            Y_prun.append(pno)
            #X_time.append(burst+arrival)          
            #Y_prun.append(0)
            prevX = arrival+burst
        else:
            X_time.append(prevX)
            Y_prun.append(pno)
            X_time.append(prevX+burst)          
            Y_prun.append(pno)
            #X_time.append(prevX+burst)          
            #Y_prun.append(0)
            prevX = prevX+burst
        # P.runing
        
        output[pno] = [pno,arrival,burst,prevX,(prevX-arrival-burst),(prevX-arrival),(prevX-arrival)/burst]
        AccumTime = prevX
    
    X_time.append(prevX)
    Y_prun.append(0)
    return
    



def DO_RR():
    output.clear()
    X_time.clear()
    Y_prun.clear()
    CSTime = context_val.get()
    QUANTM = quantum_val.get()    
    # Sorting with respect to Arrival Time
    datacpy = copy.deepcopy(data)
    sorted_data = sorted(datacpy.items(), key=lambda kv: kv[1][0])
    pnum = (len(sorted_data))    
    # Process No.  ( Arriv , Runing , Priority )
    prevX = 0 #sorted_data[0][1][0] ## First arrival time
    j = 1
    RRQ = []
    RRQ.append(sorted_data[0])
    while (len(RRQ) != 0):
        if (len(RRQ) == 0 and j<pnum):
            p = sorted_data[j]
            j +=1
        else:
            p =  RRQ.pop(0)
        
        pno = p[0]
        arrival = p[1][0]
        burst = p[1][1]
        if (arrival > prevX):
            # If the arrival time is greater than the previous time (prevX),
            #  it means there was an idle time.
            #  The code adds three points to the X_time and Y_prun lists to represent 
            # the idle period, the arrival of the process, and the start of its execution.
            X_time.append(prevX)
            Y_prun.append(0)
            
            X_time.append(arrival)
            Y_prun.append(0)
            
            X_time.append(arrival)
            Y_prun.append(pno)
            
            if (burst > QUANTM):
            #execute for quantum time
            # If the burst time is greater than the quantum time (QUANTM),
            #  the process will continue execution for the quantum time.
            #  The code updates prevX accordingly.
                X_time.append(arrival+QUANTM) 
                prevX = arrival+QUANTM
            else:
            #execute for burst time
            # If the burst time is less than or equal to the quantum time,
            #  the process will finish execution.
            #  The code updates prevX accordingly and calculates
            #  the waiting time, turnaround time, and normalized turnaround time for the process.
            #  It stores these values in the output dictionary with the process number as the key.
                X_time.append(arrival+burst) 
                prevX = arrival+burst
            Y_prun.append(pno)
            
        else:
            X_time.append(prevX)
            Y_prun.append(pno)
            if (burst >= QUANTM):
                X_time.append(prevX+QUANTM) 
                prevX = prevX+QUANTM
            else:
                X_time.append(prevX+burst) 
                prevX = prevX+burst
            Y_prun.append(pno)
        
        while (j < pnum and sorted_data[j][1][0] <= prevX ):
            RRQ.append(sorted_data[j])
            j +=1

        if (p[1][1] > QUANTM):
            # If the burst time of the current process in RRQ 
            # is greater than the quantum time,
            #  it reduces the burst time by the quantum time and
            #  appends the process back to RRQ for future execution.
            p[1][1] -= QUANTM
            RRQ.append(p)
        else :
            # If the burst time is less than or equal to the quantum time,
            #  it sets the burst time to 0 and retrieves
            #  the original arrival time and burst time from the data dictionary.
            #  It then calculates the waiting time, turnaround time,
            #  and normalized turnaround time for the process
            #  and stores them in the output dictionary.
            p[1][1] = 0
            p = data[int(pno)]
            arrival = p[0]
            burst = p[1]
            output[pno] = [pno,arrival,burst,prevX,(prevX-arrival-burst),(prevX-arrival),(prevX-arrival)/burst]
        
        # CONTEXT SWITCHING 
        if (CSTime != 0 and len(RRQ) != 0 and RRQ[0][0] != pno and RRQ[0][1][0] <= prevX):
            # The code then checks if there is a context switching time (CSTime) defined
            #  and if there are processes remaining in RRQ.
            #  If true, it adds two points to X_time and Y_prun to represent the context switching time.
            X_time.append(prevX)
            Y_prun.append(-1)
            X_time.append(prevX+CSTime)          
            Y_prun.append(-1)
            prevX = prevX+CSTime
        
        if (len(RRQ) == 0 and j<pnum):
            RRQ.append(sorted_data[j])
            j +=1
    X_time.append(prevX)
    Y_prun.append(0)
    return
# The context switch time affects the Round Robin (RR) algorithm by introducing
#  a delay whenever there is a switch between executing one process and moving to another.
#  Here's how the context switch time impacts the RR algorithm:

# 1. During the execution of the RR algorithm, processes are scheduled to run for
#  a fixed quantum of time (QUANTM). 

# 2. When a process's quantum time expires, it is preempted, 
# and the next process in the queue is selected to execute.

# 3. However, before switching to the next process, a context switch may occur.

# 4. A context switch refers to the overhead involved in saving
#  the current process's execution state, such as register values, 
# program counters, and other relevant information, and restoring
#  the execution state of the next process to be executed.

# 5. The context switch time represents the time taken to perform this switching operation.
# 6. In the provided code, the context switch time is denoted by the variable `CSTime`.
# 7. Whenever a context switch occurs, it introduces an additional delay in the execution timeline.
# 8. The code accounts for this delay by adding extra points in the `X_time` and `Y_prun` 
# lists to represent the context switch time.

# 9. The `X_time` list keeps track of the time points in the execution timeline,
#  while the `Y_prun` list represents the corresponding process numbers or
#  special markers for idle time and context switching.

# 10. When a context switch is required, the code appends two points in `X_time`:
#  the current time (`prevX`) and the current time plus the context switch time (`prevX + CSTime`).

# 11. In `Y_prun`, it appends `-1` for both points to indicate a context switch.
# 12. After the context switch, the execution of the next process resumes.

# 13. The context switch time has an impact on the overall scheduling of
#  processes and affects the waiting time, turnaround time, and response time of the processes.

# 14. A longer context switch time increases the overhead
#  and reduces the available execution time for the processes,
#  potentially affecting system performance and responsiveness.

# 15. It is important to consider an optimal context switch time
#  in order to minimize the impact on the overall execution of processes 
# and achieve efficient scheduling in the Round Robin algorithm.
    




def DO_SJFP():#shortest job first preemptive
    output.clear()
    output.clear()
    X_time.clear()
    Y_prun.clear()
    CSTime = context_val.get()
    QUANTM = quantum_val.get()    
    # Sorting with respect to Arrival Time
    datacpy = copy.deepcopy(data)
    sorted_data = sorted(datacpy.items(), key=lambda kv: kv[1][0])
    pnum = (len(sorted_data))    
    # Process No.  ( Arriv , Runing , Priority )
    prevX = (sorted_data[0][1][0])
    j = 1
    RRQ = []    
    RRQ.append(sorted_data[0])
    prevpid = 0
    dontswitch = 0
    while (len(RRQ) != 0):

        while (j < pnum and sorted_data[j][1][0] <= prevX ):
            RRQ.append(sorted_data[j])
            j +=1
        
        RRQ = dict(RRQ)
        RRQ  = sorted(RRQ.items(), key=lambda kv: kv[1][1])

        if (len(RRQ) == 0 and j<pnum):
            p = sorted_data[j]
            j +=1
        else:
            p =  RRQ[0]
        
        pno = p[0]
        arrival = p[1][0]
        burst = p[1][1]
        if (arrival > prevX):
            X_time.append(prevX)
            Y_prun.append(0)
            
            X_time.append(arrival)
            Y_prun.append(0)
            
            X_time.append(arrival)
            Y_prun.append(pno)
            
            if (burst > QUANTM):
                X_time.append(arrival+QUANTM) 
                prevX = arrival+QUANTM
            else:
                X_time.append(arrival+burst) 
                prevX = arrival+burst
            Y_prun.append(pno)
            
        else:
            X_time.append(prevX)
            Y_prun.append(pno)
            if (burst >= QUANTM):
                X_time.append(prevX+QUANTM) 
                prevX = prevX+QUANTM
            else:
                X_time.append(prevX+burst) 
                prevX = prevX+burst
            Y_prun.append(pno)
        
        if (p[1][1] > QUANTM):
            p[1][1] -= QUANTM
        else :
            RRQ.pop(0)
            p[1][1] = 0
            p = data[int(pno)]
            arrival = p[0]
            burst = p[1]
            output[pno] = [pno,arrival,burst,prevX,(prevX-arrival-burst),(prevX-arrival),(prevX-arrival)/burst]
            if (len(RRQ) == 0 and j<pnum):
                RRQ.append(sorted_data[j])
                j += 1

        # CONTEXT SWITCHING 
        if (CSTime != 0 and len(RRQ) != 0 and RRQ[0][0] != pno and RRQ[0][1][0] <= prevX):
            X_time.append(prevX)
            Y_prun.append(-1)
            X_time.append(prevX+CSTime)          
            Y_prun.append(-1)
            prevX = prevX+CSTime
    
    X_time.append(prevX)
    Y_prun.append(0)
    
    return



def update_graph():
    # Figure 
    figure = Figure(figsize=(13, 5), dpi=100)
    plot = figure.add_subplot(1, 1, 1)
    
    # Fetch selected algorithm
    ALGORITHM = algo.cget("text")
    if ALGORITHM=="HPF":
        DO_HPF()
    elif ALGORITHM=="FCFS":
        DO_FCFS()
    elif ALGORITHM=="RR":
        DO_RR()
    elif ALGORITHM=="SJFP":
        DO_SJFP()
    
    # Draw Output
    plot.set_title (algo.cget("text"), fontsize=16)
    plot.set_ylabel("Process No.", fontsize=14)
    plot.set_xlabel("Time", fontsize=14)
    
    x = X_time
    y = Y_prun
    plot.step(x, y, color="blue", linestyle="-")
    plot.grid(visible=True, which='major', color='#AAAAAA', linestyle='-')
    plot.set_yticks(y)
    plot.set_xticks(x)
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.get_tk_widget().grid(row=4, column=0,padx=5, pady=5,columnspan=4, sticky="news")

    return




def output_write():
    output_path = output_val.get()
    file = open(output_path, "w")
    pnum = len(output)
    ALGORITHM = algo.cget("text")
    if ALGORITHM=="HPF":
        file.write("CPU sheduling according to Highest priority first algorithm"+'\n\n')
    elif ALGORITHM=="FCFS":
        file.write("CPU sheduling according to First come First serve algorithm"+'\n\n')
    elif ALGORITHM=="RR":
        file.write("CPU sheduling according to Round robin algorithm"+'\n\n')
    elif ALGORITHM=="SJFP":
        file.write("CPU sheduling according to Shortest Job first preemtive algorithm"+'\n\n')
    file.write("Process Count : "+str(pnum)+'\n')
    avg_ta = 0
    avg_wta = 0
    file.write("P. No\t\t"+"Arrival time\t"+"Burst time\t"+"Completion time\t"+"Waiting time\t"+"Turn-around time\t"+"Waiting-time-average"+'\n')
    for i in (output.keys()):
        #print(p[1])
        p = output[i]
        #print(p)
        avg_ta += p[5]
        avg_wta += p[4]
        file.write(str(i)+"\t\t"+str(p[1])+"\t\t"+str(p[2])+"\t\t"+str(p[3])+"\t\t"+str(p[4])+"\t\t"+str(p[5])+"\t\t\t"+str(p[6])+'\n')
    file.write("\nAvgerage Turn-around time :" +str(avg_ta/pnum)+"\n"+"Average Waiting time:"+str(avg_wta/pnum)+'\n')
    messagebox.showinfo("Outputfile status","Successfully Written .")
    file.close()
    
 


# GLOBAL VARS
data = {}
output = {}

# Process Number/Count
pnum = 0

# Time slots
X_time = []
# Runing Process No.
Y_prun = []

root = Tk(className=' OS Scheduler')
#root.geometry("860x640")
#root.resizable(width=False, height=False)
filename=""



# Label-Input Context Switching
context_label = Label(root,text='Context Switch Time :')
context_label.grid(row=0 ,column=0,padx=5, pady=10,ipadx=5,sticky='w')



#context_time = StringVar(root)
context_val = IntVar(root, value=0)
context_entry = Entry (root,textvariable=context_val) #validate='key')
context_entry.grid(row=0,column=1,ipadx=5,sticky="w")




# Label-Input Time Quantum
quantum_label = Label(root,text='Quantum Time :')
quantum_label.grid(row=1 ,column=0,padx=12, pady=10,ipadx=5,sticky='w')
quantum_val = IntVar(root, value=1)

quantum_entry = Entry (root,textvariable=quantum_val)
quantum_entry.grid(row=1,column=1,ipadx=5,sticky="w")



# Show/Update Btn
update_btn = Button(root,text="Show/Update Graph",command=update_graph)
update_btn.grid(row=2,column=0,padx=5, pady=10,ipadx=5,columnspan=1,sticky='w')



# Open file Btn
browse_btn = Button(root,text="Select Input File",command=browse_input)
browse_btn.grid(row=3,column=0,padx=5,ipadx=19,columnspan=1,sticky='w')




# Show opened file path
file_label = Label(root,text='File Path: '+filename)
file_label.grid(row=5,column=0)

path_label = Label(root,text=filename)
path_label.grid(row=5,column=1)




# Drop down list for algorithm selection
OPTIONS = ["SELECT ALGORITHM","HPF","FCFS","RR","SJFP" ] 

variable = StringVar(root)
variable.set(OPTIONS[0]) # default value

algo = OptionMenu(root, variable, *OPTIONS)
algo.grid(row=2,column=1,sticky='w')



#Outputfile 
output_label = Label(root,text='Output file name :')
output_label.grid(row=3 ,column=1,sticky="w")
output_val = StringVar(root, value="Out.txt")

output_entry = Entry (root,textvariable=output_val)
output_entry.grid(row=3,column=2,sticky="w")

write_btn = Button(root,text="Write File",command=output_write)
write_btn.grid(row=3,column=3,padx=5,ipadx=19,columnspan=1,sticky='w')



# Graph
figure = Figure(figsize=(13, 5), dpi=100)
plot = figure.add_subplot(1, 1, 1)

plot.set_title (algo.cget("text"), fontsize=16)
plot.set_ylabel("Process No.", fontsize=14)
plot.set_xlabel("Time", fontsize=14)
x = X_time
y = Y_prun

plot.step(x, y, color="blue", marker=".", linestyle="")
plot.grid(visible=True, which='minor', color='#AAAAAA', linestyle='-')
plot.set_yticks(y)
plot.set_xticks(x)

canvas = FigureCanvasTkAgg(figure, root)
canvas.get_tk_widget().grid(row=4, column=0,padx=5, pady=5,columnspan=4, sticky="news")

# Main loop

root.mainloop()





















