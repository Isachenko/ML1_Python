# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <rawcell>

# NN

# <rawcell>

# Activation functions

# <codecell>

from math import exp

def F_threshold_binary(s):
    y = 0 if s <=0 else 1
    return y

def F_threshold_bipolar(s):
    y = -1 if s<=0 else 1
    return y

def F_sigmoidal_binory(s, param = 1):
    y = 1 / (1+(exp(param * s)))
    return y
    
def F_sigmidal_bipolar(s, param = 1):
    y = (2 / (1+(exp(param * s)))) - 1;
    return y

def F_hiperbolic_tg(s):
    return F_sigmidal_bipolar(s, 2)

def F_linear(s):
    return s

# <rawcell>

# Alpha (learning step)

# <codecell>

def step_constant_small(_):
    return 0.01

def step_constant_medium(_):
    return 0.1

def step_constant_large(_):
    return 0.5

def step_adaptive(x):
    s = sum(xi**2 for xi in x)
    return 1.0 / (1 + s)

# <codecell>

import math
import matplotlib.pyplot as plt
from random import random, shuffle


def generate_dots(centerX1, centerX2, size, maxr, name):    
    points = []
    for i in range(size):
        r = random()*maxr
        alf = random()*(2*math.pi)
        x1 = centerX1 + r*math.sin(alf)
        x2 = centerX2 + r*math.cos(alf)
        points.append((x1, x2, name))
        
    return points

def generate_sin_dots(a, b, c, size, step):    
    points = []
    t = 0
    for i in range(size):
        t = t + step
        y = a * math.sin(b * t) + c;
        points.append((t, y))
        
    return points
    

def count_weights(points, exitNeuronNum):
    shuffle(points)
    w1 = w2 = T = 0.1
    cur_epoch = 0
    good_epoch = False
    while(not good_epoch):
        good_epoch = True
        for cur_point in points:
            alf = step_adaptive(cur_point[0: 1])
            S = cur_point[0]*w1 + cur_point[1]*w2 - T
            y = F_threshold_binary(S)
            name_e = (cur_point[2] >> exitNeuronNum) % 2
            K = y - name_e
            w1 = w1 - (alf * cur_point[0] * K)
            w2 = w2 - (alf * cur_point[1] * K)
            T = T + (alf * K)
            if K != 0:
                good_epoch = False
        cur_epoch = cur_epoch + 1
        if (good_epoch):
            break
        #if (cur_epoch > 1000):
        #    break
    a = -w1/w2
    b = T/w2
    print cur_epoch
    return a, b

class perceptrone:
    def __init__(self, inCount):
        self.in_count = inCount
        self.w = []
        self.T = 1;
        
        self.alf = 0.1
            
    def teach(self, inputs, outputs, Ee):
        self.w = [0.1 for x in range(self.in_count)]
        cur_epoch = 0
        good_epoch = False
        while(not good_epoch):
            good_epoch = True
            j = 0
            for cur_input in inputs:
                #alf = step_adaptive(cur_point[0: 1])
                S = 0
                i = 0
                for xi in cur_input:
                    S = S + xi*self.w[i]
                    i = i + 1;
                S = S - self.T
                y = F_linear(S)
                K = y - outputs[j]
                i = 0
                for wi in self.w:
                    wi = wi - (self.alf * cur_input[i] * K)
                    i = i + 1;
                self.T = self.T + (self.alf * K)
                j = j + 1
            Es = 0
            j = 0
            for cur_input in inputs:
                S = 0
                i = 0
                for xi in cur_input:
                    S = S + xi*self.w[i]
                    i = i + 1;
                S = S - self.T
                y = F_linear(S)
                Es = Es + (y - outputs[j])**2
            Es = Es / 2
            if (Es < Ee):
                good_epoch = False
            cur_epoch = cur_epoch + 1
            if (good_epoch):
                break
            if (cur_epoch > 3000):
                break
        print cur_epoch
        
    def get_prophecy(self, sample):
        i = 0
        S = 0
        for xi in sample:
            S = S + xi*self.w[i]
            i = i + 1;
        S = S - self.T
        y = F_linear(S)
        return y
        
        
    
        
        
    

# <codecell>

a = generate_dots(0, 0, 10, 2.1, 0)
b = generate_dots(7, 5, 10, 2.1, 1)
c = generate_dots(5, 0, 10, 2.1, 2)
d = generate_dots(5, 5, 10, 2.1, 3)

dots = []
dots.extend(a)
dots.extend(b)
dots.extend(c)
dots.extend(d)

l1, m1 = count_weights(dots, 0)
#l2, m2 = count_weights(dots, 1)


a = zip(*a)
b = zip(*b)
#c = zip(*c)
#d = zip(*d)


plt.plot(a[0], a[1], 'ro')
plt.plot(b[0], b[1], 'bo')
#plt.plot(c[0], c[1], 'yo')
#plt.plot(d[0], d[1], 'go')
plt.plot((-10, 10), (-10*l1+m1, 10*l1+m1),color='black')
#plt.plot((-10, 10), (-10*l2+m2, 10*l2+m2),color='black')

plt.axis([-10, 10, -10, 10])

plt.show()

# <codecell>


def solve_problem(lenght, steps_count, window_size):
    step_length = lenght / steps_count
    p = generate_sin_dots(1, 1, 0, steps_count, step_length);
    p = zip(*p)
    sample_size = steps_count - window_size
    sample = []
    answers = []
    for i in range(0, sample_size) :
        sample.append(p[1][i : i + window_size])
        answers.append(p[1][i + window_size])
    prc = perceptrone(len(sample[0]))
    prc.teach(sample, answers, 10)
    
    x = 10.5*math.pi
    y = prc.get_prophecy(p[1][sample_size: sample_size + window_size])

    plt.plot(p[0], p[1], 'ro')
    plt.plot(x, y, 'bo')
    plt.axis([-1, 11*math.pi, -1, 1])
    
    plt.show()
    
                        
    
    
    
solve_problem(10*math.pi, 300, 5)
    



# <codecell>

print x

