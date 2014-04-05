import os, sys, traceback, getpass, time, re
from random import random
from random import random,randint
import threading
from threading import Thread,Condition
from subprocess import *
import math


PARTICLE=35
def conversion(num):
  binary="{0:b}".format(num)
  binary=binary[::-1]
  numbers=[]
  for i in range(0,len(binary)):
    if binary[i] == '1':
      numbers.append(i)
  return numbers
  
def subfile(a,i):
  f=open("test1","r")
  fo = open("foo%d.txt" %i, "w+")
  while 1:
    line=f.readline()
    line1=line.split(" ")
    if not line:break
    string=line1[0]+" "
    for j in a:
      string=string + " ".join(line1[2*j+1:2*j+3])+" "
    string=string+'\n'
    fo.write(string)
  fo.close()
  f.close()
  
  
sync=[0]*PARTICLE
c1=c2=1.35
gBest=[0,0]
sync=[0]*PARTICLE
lBest=[0]*PARTICLE
particles=[]
#particles=[1, 2, 3, 5, 6]
for i in range(0,PARTICLE):
  particles.append(randint(1,2**65))
  
#pBest=[ [0] * 3 ] * 20
#pBest=[[0]*2]*PARTICLE
#for i in range(0,PARTICLE):
#  pBest[i][0]=0
#  pBest[i][1]=0
pBest=[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
#pBest=[[0,0],[0,0],[0,0],[0,0],[0,0]]

def Training(c):
  cmdline = '../svm-train -v 10 %s' %c
  result = Popen(cmdline,shell=True,stdout=PIPE,stderr=PIPE,stdin=PIPE).stdout
  for line in result.readlines():
    if str(line).find('Cross') != -1:
      return float(line.split()[-1][0:-1])

def __pso(i):
  loop=0
  
  while(loop<10):
    if i == 0:
      print
      print "loop %d Current particles %s" %(loop,particles)
      print '************************************************'
    mem=0
    subfile(conversion(particles[i]),i)
    if particles[i] != gBest[0] and pBest[i][0]!=particles[i]:
      lBest[i] = Training("foo%d.txt"%i)
    cv.acquire()
    if lBest[i]> pBest[i][1]:
      pBest[i][1]=lBest[i]
      pBest[i][0]=particles[i]
      if lBest[i]> gBest[1]:
        gBest[1]=lBest[i]
        gBest[0]=particles[i]
    print "lbest", lBest
    print "Pbest",pBest
#    print gBest
    print sync
    sync[i]+=1   
    for mem in range(PARTICLE):
      if sync[mem]<sync[i]:
        cv.wait()
    if sync[mem]==sync[i] and mem==PARTICLE-1:
        cv.notifyAll()
    particles[i]=int(math.ceil((particles[i]+c1*randint(0,1)*(pBest[i][0]-particles[i])+c2*randint(0,1)*(gBest[0]-particles[i]))))
    if particles[i]<0:
      particles[i]=0
    cv.release()
    if i == 0:
      print "global best %s features %s at end of loop %d" %(gBest,conversion(gBest[0]),loop)
    loop=loop+1

if __name__ == '__main__':
  threads=[]
  cv = Condition()
  for i in range(PARTICLE):
    t = threading.Thread(target=__pso, args=(i,))
    threads.append(t)
    t.start()
