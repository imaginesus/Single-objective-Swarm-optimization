from numpy import array
from random import random
from math import sin, sqrt

iter_max = 10
pop_size = 50
dimensions = 2
c1 = 2
c2 = 2
err_crit = 0.00001 
x_low = -10
x_high = 10

def func(param):
    '''we use sphere function'''
    sphere_value = 0
    for i in range(dimensions):
        sphere_value+= (param[i])**2
    f = dimensions*100 - sphere_value
    return f,sphere_value;

def neighbor(solution):
     
     a = random()
     if random() > 0.5:
         
         if a > 0.5:
             solution[0] = solution[0]-0.05
         else:
             solution[0] = solution[0]+0.05
 
     else:
         if a > 0.5:
             solution[1] = solution[1]-0.05
         else:
             solution[1] = solution[1]+0.05
 
     return solution
  
def acceptance_probability(old_cost, new_cost, T):
	e = 2.718
	diff = (old_cost - new_cost)/T
	ap = e**diff
	return ap
def anneal(solution,T):
    old_error,old_cost = func(solution)
    
    T_min = 0.00001
    alpha = 0.9
    while T > T_min:
        i = 1
        while i <= 100:
            solut = [0,0]
            solut = solut+solution
            new_solution = neighbor(solut)
            new_error,new_cost = func(new_solution)
            ap = acceptance_probability(old_cost, new_cost, T)
            if ap > random():
                solution = new_solution
                old_cost = new_cost
            i += 1
        T = T*alpha
        
    return solution, old_cost,old_error

#initialize the particles randomly in the search space and set velocity and other parameters zero initialy
class Particle:
    pass
particles = []
for i in range(pop_size):
    p = Particle()
    p.params = array([random() for i in range(dimensions)])
    p.fitness = 0.0
    p.error = 99999999
    p.v = [0.0,0.0]
    p.t = 0.0
    p.best = [0,0]
    particles.append(p)
 
# let the first particle be the global best
gbest = particles[0]
err = 999999999
while i < iter_max :
    k=0
    wt = 1
    for p in particles:
 
        fitness,err = func(p.params)
        if err< p.error:
            p.fitness = fitness
            p.best = p.params
            p.error = err
 
        if err < gbest.error:
            gbest = p
            
        v = p.v + c1 * random() * (p.best - p.params) + c2 * random() * (gbest.params - p.params)
        p.params = p.params + v
 
        if p.params[0] >x_high or p.params[0]<x_low or p.params[1] >x_high or p.params[1]<x_low:
        	del particles[k]
        	
        k = k+1
    
    gbest_fit,gbest_err = func(gbest.params)
    
    i  += 1
    if gbest_err < err_crit:
        break
    #progress bar. '.' = 10%
    if i % (iter_max/10) == 0:
        print '.'
 
# Allot each particle a temperature value based on its velocity to apply simulated annealing
temperature_arr =[]
for p in particles:
    p.v =  c1 * random() * (p.best - p.params) \
                + c2 * random() * (gbest.params - p.params)
    p.t = p.v[0]**2+p.v[1]**2
    temperature_arr.append(p.t)

for fillslot in range(len(temperature_arr)-1,0,-1):
    positionOfMax=0
    for location in range(1,fillslot+1):
        if temperature_arr[location]>temperature_arr[positionOfMax]:
            positionOfMax = location

    temp = temperature_arr[fillslot]
    temp1 = particles[fillslot]
    temperature_arr[fillslot] = temperature_arr[positionOfMax]
    particles[fillslot] = particles[positionOfMax]
    temperature_arr[positionOfMax] = temp
    particles[positionOfMax] = temp1

#divide the particles among three zones and consider avg. temperature for annealing
t1,t2,t3 = 0,0,0
for p in particles[0:(len(particles))/3]:
    t1 = t1 + (p.t)
for p in particles[(len(particles))/3:2*(len(particles))/3]:
    t2 = t2 + (p.t)
for p in particles[2*(len(particles))/3:]:
    t3 = t3 + (p.t)

t1,t2,t3 = sqrt(t1),sqrt(t2),sqrt(t3)
gbest_params,gbest_error = gbest.params,gbest.error
best_fit1,best_fit2,best_fit3 = 0,0,0
best_loc1,best_loc2,best_loc3 = [0,0],[0,0],[0,0]

#proceed to anneal the three zones to improve solution values
for p in particles[1:(len(particles))/3]:
    loc,err,fit = anneal(p.params,t1)
    if fit > best_fit1:        
        best_fit1 = fit
        best_loc1 = loc        
print 't1 ',t1,'error',200-best_fit1

for p in particles[(len(particles))/3:2*(len(particles))/3]:
    loc,err,fit = anneal(p.params,t2)
    if fit > best_fit2:        
        best_fit2 = fit
        best_loc2 = loc
print 't2 ',t2,'error',200-best_fit2

for p in particles[2*(len(particles))/3:]:
    loc,err,fit = anneal(p.params,t3)
    if fit > best_fit3:        
        best_fit3 = fit
        best_loc3 = loc
print 't3 ',t3,'error',200-best_fit1 

###############################################################################
print 'Population size : ', pop_size
print 'Dimensions      : ', dimensions
print 'gbest params    : ', gbest_params
print 'pso_fitness, pso_error   : ', gbest.fitness, gbest_error
print 'pso_sa fitness, pso_sa_error'
if best_fit1>best_fit2:
    if best_fit1>best_fit3:
        print best_fit1,200-best_fit1
    else:
        print best_fit3,200-best_fit3
else:
    if best_fit2>best_fit3:
        print best_fit2,200-best_fit2
    else:
        print best_fit3,200-best_fit3
###############################################################################