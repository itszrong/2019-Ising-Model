import numpy as np
import random
import matplotlib

#Inverse Boltzmann constant
Inv_Kb = (1.380649)*(10)**(23)
#temperature
T = 0.00000000000000000000001
#beta is inverse temperature
#BETA = 3.5*Inv_Kb/T
BETA = 75

#location of neighbours if middle if sigma ij on a cartesian plane
dx = [-1, 0, 1, 0]
dy = [0 , -1, 0, 1]

#convert into spins
def get(i):
    if i: return 1
    else: return -1

#computing the hamiltonian
def h(config):
    total = 0
    rows = config.shape[0]
    cols = config.shape[1]
    #to compute for every spin
    for i in range(rows):
        for j in range(cols):
            #each of 4 neighbours
            for k in range(len(dx)):
                nx = i + dx[k]
                ny = j + dy[k]
                if nx < 0 or ny<0 or nx>= rows or ny >= cols:
                    #ensures within matrix
                    continue

                val = get(config[i][j]) * get(config[nx][ny])
                total += val

    return total #energy to find prob

def nexts(config, i, j, HAM): #energy level of new stage after one swap
    #take size (x, y)
    rows = config.shape[0] #x
    cols = config.shape[1] #y
    total = HAM
    for k in range(len(dx)): #do it for 4 neighbours
        nx = i + dx[k]
        ny = j + dy[k]
        if nx < 0 or ny<0 or nx>= rows or ny >= cols:
            continue

        val = get(config[i][j]) * get(config[nx][ny]) # contribution from one spin
        next = get(not config[i][j]) * get(config[nx][ny]) #energy of new spin
        total += val #subtract and add new value
        total -= next
    return total
    #next energy

#finding the relative probability
def relprob(u, v):
    return np.exp(BETA * ( u- v ))
def accept(u, v): #u is ham, v is new
    r = random.random() #generates a random number between 0 and 1
    return r<relprob(u, v)
#accept 
def step(config, HAM):
    rows = config.shape[0]
    cols = config.shape[1]
    i = random.randrange(0, rows)
    j = random.randrange(0, cols)
    next = np.copy(config) #take position
    next[i][j] = not next[i][j] # flips spin
#change spin of a random particle
    new = nexts(config, i, j, HAM) 
    #ns is total from nexts

    if accept(HAM, new):
        config = np.copy(next)#actually changing it
    return config #returns true or false

def initialise():
    #initialise system
    current = np.random.choice(a=[0, 1], size=(50, 50)) #create matrix and true and false, current is the matrix
    HAM = h(current) #take the ham
    #thermalisation
    print('therm')
    import matplotlib.pyplot as plt
    for i in range(10000): #therm
    #    print(i)
        #do many steps
        cur = step(current, HAM)
    samples = [] #to store
    import time # for pause
    #toggle
    colors = ['red', 'blue']
    bounds = [0,1] #asign values

    cmap = matplotlib.colors.ListedColormap(colors)
    norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

    for i in range(10000):#take sample every 1000 steps
    #    print(i)
        for j in range(100): #output in terminal
            current = step(current, HAM)
    #take sample
        samples.append(np.copy(current)) #add samples to samples
    #    plt.subplot(211)
    #    plt.imshow(current, cmap=cmap)#display into graph
    #cur is current
    #    plt.show(block=False)
    #    plt.pause(0.01)
        #plt.close()
    Average_Magnetisation = M(samples)
    return Average_Magnetisation

#compute magnetistation 
def M(samples):
    Magnetisation_samples = []
    Average_Magnetisation = 0
    rows = samples[1].shape[0]
    cols = samples[1].shape[1]
    for n in range (len(samples)):
        total_M = 0
        #to compute for every spin
        for i in range(rows):
            for j in range(cols):
                total_M += get(samples[n][i][j])

        Magnetisation_samples.append(total_M/(rows*cols))
    
    for n in range (len(Magnetisation_samples)):
        Average_Magnetisation += Magnetisation_samples[n]
    Average_Magnetisation = Average_Magnetisation/len(Magnetisation_samples)
    print(Magnetisation_samples)
    return Average_Magnetisation

Magnetisation = 0
j=10
for i in range (j):
    Magnetisation_for_sample = initialise()
    Magnetisation += Magnetisation_for_sample

Actual_average_magnetisation = Magnetisation/j 
print ("Magnetisation is ", Actual_average_magnetisation)

