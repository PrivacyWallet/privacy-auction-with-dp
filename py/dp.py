import math
import operator
import numpy
import random
# import matplotlib.pyplot as plt
def count(counts,epsilons):
    size=len(epsilons)

    count=[]
    epsilon=[]
    for i in range(0,size):
        count.append(int(counts[i]))
        epsilon.append(float(epsilons[i]/100))
    epsilon_zero=[]
    epsilon_one=[]
    d_count=[0 for i in range(size+1)]
    x=0
    for i in range(0,size):
        if(count[i]==1):
            x=x+1
            epsilon_one.append(epsilon[i])
        else:
            epsilon_zero.append(epsilon[i])
    epsilon_one.sort(reverse = True)
    epsilon_zero.sort(reverse = True)
    for i in range(0,size+1):
        if(i<x):    
            num=x-i
            for j in range(0,num):
                d_count[i]-=epsilon_one[j]
        elif(i>x):
            num=i-x
            for j in range(0,num):
                d_count[i]-=epsilon_zero[j]
        elif(i==x):
            d_count[i]=0
    sum1=0
    pos=[0 for i in range(size+1)]
    for i in range(0,size+1):
        pos[i]=math.exp(0.5*d_count[i])
        sum1+=math.exp(0.5*d_count[i])
    for i in range(0,size+1):
        pos[i]=pos[i]/sum1
    a2 = numpy.random.choice(a=[i for i in range(0,size+1)], size=1, replace=False, p=pos)
    if(a2[0]<1):
        res=0
    else:
        res=a2[0]-1
    print("count is "+str(x)+", and result is "+str(res))
    return res
def median(nums,epsilons):
    quantity=len(epsilons)
    epsilon=[]
    data=[]
    for i in range(0,quantity):
        data1=(int(nums[i]),float(epsilons[i]))
        data.append(data1)
        epsilon.append(float(epsilons[i]/100))
    data.sort(key=lambda x:x[0],reverse=False)
    lo=data[0][0]
    hi=data[quantity-1][0]
    size=hi-lo+1
    mid=quantity//2
    pos=[0 for i in range(size)]
    pos1=[0 for i in range(size)]
    for i in range(0,size):
        number=i+lo
        #print(number)
        if number <data[mid][0]:
            loc=0
            for j in range(0,quantity):
                if number>=data[j][0]:
                    loc=j
        #print(loc)
            epsilon_tmp=[epsilon[i] for i in range (loc+1,quantity)]
            epsilon_tmp.sort(reverse = True)
        #print(epsilon_tmp)
            times=mid-loc
        #print(times)
            for j in range(0,times):
                pos[i]-=epsilon_tmp[j]
        #print(pos[i])
            pos[i]=math.exp(0.5*pos[i])
        elif (number==data[mid][0]):
            pos[i]=math.exp(0)
        #print(number)
        elif number>data[mid][0]:
            loc=0
            for j in range(0,quantity):
                if number>data[j][0]:
                    loc=j+1
            epsilon_tmp=[epsilon[i] for i in range (0,loc+1)]
            epsilon_tmp.sort(reverse = True)
        #print(epsilon_tmp)
            times=loc-mid
        #print(times)
            for j in range(0,times):
                pos[i]-=epsilon_tmp[j]
            pos[i]=math.exp(0.5*pos[i])
    sum=0
    for i in range(0,size):
        sum+=pos[i]
    for i in range(0,size):
        pos1[i]=pos[i]/sum
    a2 = numpy.random.choice(a=[i for i in range(lo,hi+1)], size=1, replace=False, p=pos1)
    print("mid is "+str(data[mid][0])+", choice is "+str(a2[0]))
    return(a2[0])
def min(nums,epsilons):
    quantity=len(epsilons)
    epsilon=[]
    data=[]
    for i in range(0,quantity):
        data1=(int(nums[i]),float(epsilons[i]))
        data.append(data1)
        epsilon.append(float(epsilons[i]/100))
    data.sort(key=lambda x:x[0],reverse=True)
    lo=data[0][0]
    hi=data[quantity-1][0]
    size=-(hi-lo+1)
    mid=0
    pos=[0 for i in range(0-size,size)]
    pos1=[0 for i in range(0-size,size)]
    for i in range(0-size,size):
    #print(number)
        if i <data[mid][0]:
            epsilon_tmp=[epsilon[i] for i in range (0,size)]
            tmp=0
            for j in range(0,size):
                tmp-=epsilon_tmp[j]
            pos[i+size]=math.exp(0.5*tmp)
        elif (i==data[mid][0]):
            pos[i+size]=math.exp(0)
        elif i>data[mid][0]:
            loc=0
            for j in range(0,quantity):
                if i>data[j][0]:
                    loc=j+1
            epsilon_tmp=[epsilon[i] for i in range (0,loc+1)]
        #print(epsilon_tmp)
            times=loc-mid
            #print(loc,i,times)
            for j in range(0,times):
                pos[i+size]-=epsilon_tmp[j]
            #print(pos[i+size])
            pos[i+size]=math.exp(0.5*pos[i+size])
    sum=0
    for i in range(0-size,size):
        sum+=pos[i]
    for i in range(0-size,size):
        pos1[i]=pos[i]/sum
    a2 = numpy.random.choice(a=[i for i in range(0-size,size)], size=1, replace=False, p=pos1)
    print("min is "+str(data[mid][0])+", choice is "+str(a2[0]))
    return a2[0]
