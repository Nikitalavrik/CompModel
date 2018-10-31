from random import uniform
from time import time
from math import sqrt
from numpy import arange

class Task:

    def __init__(self, t_solve, t_in_sys, t_in_ord):
        
        self.t_solve = t_solve
        self.t_in_sys = t_in_sys
        self.t_in_ord = t_in_ord

def generate_Tasks(iteration, nu):
    return [Task(0.5 + uniform(0.5, nu) * (nu - 0.5), 0, 0) for i in range(iteration)]

def FIFO(tasks, lamda):
    
    m = 0
    j = 0
    point = time()

    for k in arange(1, len(tasks) + 1, lamda):

        if ((k - m) >= 1):
            j = 1
            
            for i in range(int(m), int(k)):

                if (i != 0):
                    tasks[i].t_in_ord = time() - point + tasks[i - j].t_in_sys
                    tasks[i].t_in_sys = tasks[i].t_solve + tasks[i].t_in_ord
                else:
                    tasks[i].t_in_sys = tasks[i].t_solve
                j += 1
            m = k

    return tasks

def FB(tasks, lamda, tk):
    m = 0
    j = 0
    point = time()
    stacks = [[0]] * 20
    stacks[0] = tasks

    for stack in range(len(stacks)):

        if (stacks[stack] == 0):
            break ;

        for k in arange(1, len(stacks[stack]) + 1, lamda):

            if ((k - m) >= 1):
                j = 1                
                for i in range(int(m), int(k)):     

                    if (i != 0):
                        tasks[i].t_in_ord = time() - point + tasks[i - j].t_in_sys
                        if (tasks[i].t_solve <= tk):

                            tasks[i].t_in_sys = tasks[i].t_solve + tasks[i].t_in_ord
                        else:
                            tasks[i].t_in_sys = tk + tasks[i].t_in_ord
                            tasks[i].t_solve -= tk
                            stacks[stack + 1].append(tasks[i])
                    else:
                        tasks[i].t_in_sys = tasks[i].t_solve
                    j += 1
                m = k

    print(len(stacks))
    return tasks

def average_time_in_sys(tasks):
    return sum(t.t_in_sys for t in tasks) / len(tasks)

def dispersion(tasks, aver):
    ret = sqrt(sum(((aver - t.t_in_sys)**2 for t in tasks)))
    return ret / len(tasks)

def average_time_in_order(tasks):
    return sum(t.t_in_ord for t in tasks) / len(tasks)

def calc_function(x1, x2, x3):
    return (-3) * x1 + (-1) * x2 + (-6) * x3

def get_Xx(tasks):
    aver_in_sys = average_time_in_sys(tasks)
    disp = dispersion(tasks, aver_in_sys)
    aver_in_order = average_time_in_order(tasks)
    func = calc_function(aver_in_sys, disp, aver_in_order)

    print("Average time in system     x1 - ", aver_in_sys)
    print("Dispersion time in system  x2 - ", disp)
    print("Average time in order      x3 - ", aver_in_order)
    print("Function                   f  - ", func)
    print()

k = 10000
nu = 5
lamda = 1


tasks = generate_Tasks(k, nu)
print(sum(t.t_solve for t in tasks) / len(tasks))
tasksFB = FB(tasks, lamda, 10)
tasksFifo = FIFO(tasks, lamda)

get_Xx(tasksFifo)
get_Xx(tasksFB)