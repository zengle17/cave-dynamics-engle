# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys

counter = 0 

while counter < 50:
    counter += 1
    
if counter == 50:
    print "50"
else:
    print "error"
#%%  
    
# double == is asking a question
# single = sets a command
# == same value
# >  greater than
# <  less than
# >= greater than or equal to
# <= less than or equal to 
#%%    
 #loops in python
#for
for i in range(7):
    print i
#while  \
i = 0
while (i<7):
    print i
    i += 1
#%%
#statements
#if
if a == True:
    print "cat"
#elif
elif a == False:
    print "dog"
#else
else:
    print "??"
#%%

n_velociraptors = 2
n_humans = 25
n_humans - n_velociraptors     #type n then tab to type quickly!
if n_velociraptors: print "oh no!"

#%%
n_helpless_humans = 20
n_human_hunters = 5
n_velociraptors = 2 
#if there are more velociraptors than humans, they outflank and devour
#humans who are not busy holding velociraptors at bay, reproduce
if n_velociraptors > n_human_hunters:
    n_helpless_humans = 0
    n_human_hunters = 0 

else:
 n_helpless_humans += n_helpless_humans + n_human_hunters - n_velociraptors
 
#%%
 #each day, each n_velociraptors eats 2 persons
 #humans trapped for 1 week
 n_humans = 50
 n_velociraptors = 2
#for day in range (7) #creates python list [0,1,2,3,4,5,6]
 days = range (7)
 for day in days:
     n_humans -= (n_velociraptors * 2) #takes humans - 2 people per raptor
     if n_humans <= 0:  #this loop is within the for loop
         n_humans = 0   #if so does not print negative amount of humans
         break     #break means get out of current loop and move on
print n_humans     #tells how many humans left after 7 days
#%% 
    #could set above up as a while loop rather than for loop
 n_humans = 50
 n_velociraptors = 2
 days = range (7)
while day <7:
     n_humans -= (n_velociraptors * 2) #takes humans - 2 people per raptor
     if n_humans <= 0:  
         n_humans = 0  
         break     #break means get out of current loop and move on
print n_humans     #tells how many humans left after 7 days
#%%
n_cookies = (14 + 50) / 2
pie = True
cookie_monster_is_here = True
Libby_is_here = False

day = 0
while cookie_monster_is_here:
    if n_cookies >= 10:
        n_cookies -= 10
    else:
        n_cookies = 0
        cookie_monster_is_here = False
    print day, n_cookies
    day += 1
    
#libby only arrives after cookie monster leaves
Libby_is_here = True
pie = False # they have been eaten
print "pie is gone too :("
#%%
import random
day = 0
while day<6:
    n_cupcakes = 30 
    n_customers = int(10*random.random()) #a random amount of customers 
    n_cupcakes -= n_customers
    day += 1
    if n_cupcakes > 21:
        print "money"
    else n_cupcakes > 25:
        print "50 cent"
    print day, n_cupcakes
#%%
n_humans = input('how many humans are there?\n')
# this asks the use to enter in (input) the amount of humans in the console
n_velociraptors = input('how many velociraptors are there?\n')
#%%
# and... are both of these true?
# or... is one of these cases true?
# is
a = 5
b = 5
a == b #gives true
a is b #gives false
#%%
i = 0
while True:  #while is a loop... if is a statement
    if (i >= 5) and (i <= 10): #parentheses are key to order of operations
        continue #says skip next part and goes back to i=50
    print i 
    if i >= 50:
        break
#%%
#simplest infinite loop
while True:
    pass
#%%
# handling errors with ... try:  .... except:
try:
    print asdf
except: 
    print "fail!"
#this one fails.. so you can say try to a bunch of code and except to figure
    #out where the code chunk is messing up
try:
    print "asdf"
except:
    print "fail"
#this one works
#%%
    #dictionaries gives you a full list of commands
d0 = {}
d['time'] = '5PM'
d['hunger'] = 'great'
#%%
 #functions put something in and gives something out
def chomp(success):     #define funcion named chomp
    if success:
        print "leg lost"
        dino = happy
    else:
        print "whew"
        dino = sad
    return dino
#this made a function
def colored_dogs(color):
    try:
        print "my dog is" + color
        output_sucess = true
#%%
def quadratic(a, b, c):   #to make quadratic equation solver... needs a,b,c
    try: xpos = x1 = (-b + (((b**2)*(-4*a*c))**0.5)) / (2*a)
    except: xpos = None  #quad soln only works for certain parabolas
    try: xneg = x2 = (-b - (((b**2)*(-4*a*c))**0.5)) / (2*a)
    except: xneg = None
    return xpos, xneg

solution = quadratic(10, -11, 20) #10x^2 -11x + 20 is pos and above x axis
print solution
solution1 = quadratic(10, 11, -30) #now this one is below x axis and pos
print solution1, "mathematical!"
#%%
#modules contain functions and constants...ex: import random... numpy
import numpy as np  #now numpy can be called for as np rather than numpy
np.random #brings in the random function from numpy
classes #can have all the previous and variables
print "" #this can space out your console output appearance
#%%
# numpy is a module that allows us to do all math sort of things
import numpy as np

a = np.array([[1,2],[3,4]]) # this gives a list of lists
    # really gives a 2 x 2 matrix that is 1 2 3 4
print a * a

  # pyton indexes at 0 so have to add one to start at 1
  # np.arange (0,5) = np.array ([0,1,2,3,4])
#%%
Assignment 2 = data importing and processing
assignment 3 = numerical model and finite diff tech for solving diff eqs
    usually defined by the data but uses physics, chem, predictability
Assignment 4 = final project
#%%
GIT hub = share code/work in teams
    fork = create your own copy of someone's repository
    pull request = request owner of a code to incorporate your edits
#%%
PIP = kindof like an app store for python
must be typed into command console... hit windows and type cmd
pip install module_name
or
pip uninstall module_name
ex:
pip install landlab