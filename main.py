from Genetic_Algorithm import *
from Snake_Game import *

from ast import Global
import tkinter as tk  
from functools import partial   

def call_result(label_result, n1, n2):  
    global num1,num2
    num1 = (n1.get())  
    num2 = (n2.get())  
    result = int(num1)+int(num2)  
    label_result.config(text="จำนวนประชากร = {0} \n จำนวนผู้สืบทอด = {1} \n\n (กรุณากดปิดหน้าตานี้)".format(num1,num2))  
    return

num1,num2 = 0,0 
for i in range(0, 1):
    root = tk.Tk()  
    root.geometry('400x200+100+200')  
    root.title('Calculator')  
    number1 = tk.StringVar()
    number2 = tk.StringVar()
    sol_per_pop = tk.Label(root, text="sol_per_pop").grid(row=1, column=0)  
    num_generations = tk.Label(root, text="num_generations").grid(row=3, column=0) 
    entryNum1 = tk.Entry(root, textvariable=number1).grid(row=1, column=2)  
    entryNum2 = tk.Entry(root, textvariable=number2).grid(row=3, column=2)  
    labelResult = tk.Label(root)  
    labelResult.grid(row=7, column=2)  
    call_result = partial(call_result, labelResult, number1, number2)  
    buttonCal = tk.Button(root, text="กดเพิ่มยืนยันข้อมูล", command=call_result).grid(row=10, column=0)  
    root.mainloop() 

# The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
sol_per_pop = int(num1) #จำนวนประชากร
num_generations = int(num2) #จำนวนรุ่นสืบทอด
snake_motion = 10
num_weights = valur_NN #น้ำหนักของ NN W0 W1 W2 W3
plotdatagameY = []
plotdataaverage = []
plotdatagameX = []
MS = 0
SC = 0 

# Defining the population size.
pop_size = (sol_per_pop,num_weights)
#Creating the initial population.
new_population = np.random.choice(np.arange(-1,1,step=0.01),size=pop_size,replace=True)
t_start = time.time()

num_parents_mating =  int(sol_per_pop/3.3)#int((sol_per_pop-10)/2) #จำนวนการผสมพันธุ์ ต่อรุ่นสืบทอด 20
for generation in range(num_generations):
    print('##############        GENERATION ' + str(generation)+ '  ###############' )
    # Measuring the fitness of each chromosome in the population.
    fitness,MS,SC,datagamegen = cal_pop_fitness(new_population,NN_S,snake_motion,display_width,display_height, MS , SC)
    # print('#######  fittest chromosome in gneneration ' + str(generation) +' is having fitness value:  ', np.max(fitness) ,"// Gan Score : "+str(max(datagamegen))) 
    plotdatagameY.append(max(datagamegen))
    plotdataaverage.append(np.average(datagamegen))
    plotdatagameX.append(generation)
    if generation == (num_generations-1):
        t_end = time.time()
        import matplotlib.pyplot as plt
        fig = plt.figure()
        plt.plot( plotdatagameX , plotdatagameY , c='r')
        plt.plot( plotdatagameX , plotdataaverage , c='g')
        plt.title('Time Run model is : %d.%.0f minute'%(int((t_end-t_start)/60),((t_end-t_start)%60)))
        plt.ylabel('Score')
        plt.xlabel('Generation')
        plt.show()
        fig.savefig("Generation{}.png".format(MS), dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)
        from tkinter import *
        window=Tk()
        lbl=Label(window, text="Max Score is {}".format(MS), fg='red', font=("Helvetica", 16))
        lb2=Label(window, text='Generations {0} and sol per pop {1}'.format(num_generations,sol_per_pop) , font=("Helvetica", 12))# command=myEventHandlerFunction
        lb2=Label(window, text='Time Run model is : %f.2'%(t_end-t_start) , font=("Helvetica", 12))
        lbl.place(x=60, y=50) 
        lb2.place(x=20, y=100)
        lb2.place(x=20, y=150)
        window.title('Max Score of Snake Game')
        window.geometry("300x200+10+10")
        window.mainloop()
    # Selecting the best parents in the population for mating.
    parents = select_mating_pool(new_population, fitness, num_parents_mating)

    # Generating next generation using crossover.
    offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))

    # Adding some variations to the offsrping using mutation.
    offspring_mutation = mutation(offspring_crossover)

    # Creating the new population based on the parents and offspring.
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation

    
