import os, sys, traceback, getpass, time, re
from random import random,randint
import threading
from threading import Thread,Condition
from subprocess import *
c1=c2=1.2
gBest=[0,0,0]
sync=[0]*20
lBest=[0]*20
particles=[[2,-3],[4,-5],[11,-2],[6,-1],[10,-6],[-1,-7],[10,-5],[0,-5],[-3,2],[9,-4],[4,5],[6,-2],[11,3],[7,3],[5,-2],[3,0],[-2,5],[8,-6]\
,[-1,-2],[9,-1]]
#pBest=[ [0] * 3 ] * 20
pBest=[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

def Training(c,g):
  cmdline = '../svm-train -v 5 -c {0} -g {1} test1'.format(c,g)
  result = Popen(cmdline,shell=True,stdout=PIPE,stderr=PIPE,stdin=PIPE).stdout
  for line in result.readlines():
    if str(line).find('Cross') != -1:
      return float(line.split()[-1][0:-1])

def __pso(i):
  loop=0

    
  while(loop<6):

  #Sync Point
    cv.acquire()
    for mem in range(20):	
      if sync[mem]<sync[i]:
        cv.wait();
    cv.release() 
       
    if particles[i][0] != gBest[1] or particles[i][1]!=gBest[2]:
      lBest[i] = Training(2**particles[i][0],2**particles[i][1])
    if lBest[i]> pBest[i][0]:
      pBest[i][0]=lBest[i]
      pBest[i][1]=particles[i][0]
      pBest[i][2]=particles[i][1]
      if lBest[i]> gBest[0]:
        gBest[0]=lBest[i]
        gBest[1]=particles[i][0]
        gBest[2]=particles[i][1]
    
    particles[i][0]=particles[i][0]+c1*randint(0,1)*(pBest[i][1]-particles[i][0])+c2*randint(0,1)*(gBest[1]-particles[i][0])
    if particles[i][0]<-5: particles[i][0]=-5
    if particles[i][0]>13: particles[i][0]=13
    particles[i][1]=particles[i][1]+randint(0,1)*c1*(pBest[i][2]-particles[i][1])+randint(0,1)*c2*(gBest[2]-particles[i][1])
    if particles[i][1]>3: particles[i][1]=3
    if particles[i][1]<-13: particles[i][1]=-13
    cv.acquire() 
    sync[i]+=1
    cv.notify()
    print particles
    print pBest
    print gBest
    print sync
    print
    for mem in range(20):	
      if sync[mem]==sync[i] and mem==19:
        cv.notifyAll()
    cv.release()
    loop+=1

if __name__ == '__main__':
  threads=[]
  cv = Condition()
  for i in range(20):
    t = threading.Thread(target=__pso, args=(i,))
    threads.append(t)
    t.start()
