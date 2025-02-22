# -*- coding: utf-8 -*-
"""SDN_QLTR.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EIjMgFFRkHCCnXjUjj3LgqLN2cjl6sFL
"""

# input initial ni and destination node nd
# forwarding set Nc
# while(not traversed all neighbor nodes ):
#      Drij= routing depths between ni , nj
#     if nj is destination || (Drid < Drij + Drjd and Tt(i,j)>Ttheta ) push nj
# end while
# calculate Q-value for each Nc and sort
# Select nodes with leargest Q-value from Nc to Nf
# return Nf

# as per figure 4 from paper and equation 7 to 18
import math
# depth of nodes in meter
# di,d1,d2,d3=0,25,75,50
depths=[0,25,75,50]

# residual energies of n1,n2,n3 nodes in joules with respect to 100 joule
E=[1,0.4,0.8,1]

# routing depths between nodes ni and nj j={1,2,3}
Drij=[abs(depths[1]-depths[0])/(1+math.e ** (-5*E[1]))
,abs(depths[2]-depths[0])/(1+math.e ** (-5*E[2]))
,abs(depths[3]-depths[0])/(1+math.e ** (-5*E[3]))]

# routing depths between nd and nj j={1,2};
Drj3=[abs(depths[1]-depths[3])/(1+math.e**(-5*E[1])),
      abs(depths[2]-depths[3])/(1+math.e**(-5*E[2])) ]

Nc=[]
# transmission count as 6
# link utlisation LU & avg utilisation be 0.5
# LU_ratio= luse/lmax=[0.25,0.25,1] ; LU_prev=[1,0.33,0.66] #for n1,n2,n3
# LU=LU_ratio  if(abs(LU_PREV- LU_ratio))>=avg utilisation;; else LU_prev
LU=[0.25, 0.33 , 0.66]

# paket loss ratio for n1,n2,n3 is 0.5,0.16,0.33

Tlink=[math.sqrt((LU[0])**2+2*(1-0.5)**2 )/1.77 , math.sqrt((LU[1]**2)+2*(1-0.16)**2)/1.77,
       math.sqrt((LU[2])**2+2*(1-0.33)**2 )/1.77]


# success + failure = transmission count =6
Tnode=[0.5 * (6/8+E[1]),0.5 * (6/8+E[2]),0.5 * (6/8+E[3]) ]

# tdirect for types of attack
# type1attact=Tlink, type2=tdata,type3=tnode
print("tlink ",Tlink);
print("tnode ",Tnode);


# for type1 attack
for j in range(1,4):
  # tdirect if greater than avg trust= 0.5
  if(j==3 or ( Drij[2]<(Drij[j]+Drj3[j-1]) and Tlink[j-1]>0.5)):
    Nc.append(j)

print("for type 1 attack ",Nc)

Nc=[]
# for type3 attack
for j in range(1,4):
  # tdirect if greater than avg trust= 0.5
  if(j==3 or ( Drij[2]<(Drij[j]+Drj3[j-1]) and Tnode[j-1]>0.5)):
    Nc.append(j)

print("for type 3 attack ",Nc)