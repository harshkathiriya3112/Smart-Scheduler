# OS-Scheduler
Operating systems scheduling algorithms visualization.
it is an OS scheduler using different scheduling algorithms
### Getting Started
These instructions will get you a copy of the project up and running on your local machine for develoment.  
pip install requirements.txt  
(if above command doesn't work, then open requirements.txt file and manually install all the dependencies.)  
pip install tkinter  
python scheduler.py  

### Requirements
What things you need to install ?
- matplotlib
- tkinter
- numpy
### How to use?
NB - you must have an input file contains the process to be scheduled . its format is at docs/document file 
1.  Start the program 
2.  Choose an input file 
3.  Select the algorithm using the scrolling box .
4. Click on Show/Update Graph .

scheduler module is responsible for generating a schedule for the current processes in the system to specify the
CPU usage by these processes.
implemented 4 scheduling algorithms:
1. Non-Preemptive Highest Priority First.(HPF)
2. First Come First Served. (FCFS)
3. Round Robin with fixed time quantum.(RR)
4. Preemptive Shortest Remaining Time Next.(SRTN)

Library used for GUI : Tkinter  
Library used for plots : matplotlib  
Startup window for selecting (Input file) and (Selecting an algorithm to draw its corresponding scheduling  
The following output graphs is for inputfile at (testcases/SheetQuestion.txt)

0 indicates that the cpu is free  
-1 indicates that the context switching   
### 1. First come first served  
![image](https://github.com/harshkathiriya3112/Smart-Scheduler/assets/83661454/cfcf2aa7-c160-4346-adc0-c699bca8350b)

### 2. High priority first  
![image](https://github.com/harshkathiriya3112/Smart-Scheduler/assets/83661454/4886a40e-f94e-47df-82c0-d2cbb15c5c2d)

### 3. Round Robin  
![image](https://github.com/harshkathiriya3112/Smart-Scheduler/assets/83661454/7b485020-4634-4543-b6d9-55c7651fd909)

### 4. Short remaining time next  
![image](https://github.com/harshkathiriya3112/Smart-Scheduler/assets/83661454/d2d4a92f-3410-4592-ad45-79ce5422d86d)

