# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Fzi3hFhZ4gpbu1HlKgRBpnPI1zi3TtLv
"""

import warnings
warnings.filterwarnings('ignore')

import random
import math
from sklearn.cluster import KMeans
import numpy as nm
import matplotlib.pyplot as mtp
import pandas as pd
arr = [[j,j] for j in range(1,400,2)]
Energy=[2 for j in range(0,200)]

def FIND_K(arr):
  wcss_list= []
  for i in range(1, 10):
      kmeans = KMeans(n_clusters=i, init='k-means++', random_state= 42)
      kmeans.fit(arr)
      wcss_list.append(kmeans.inertia_)
  mtp.plot(range(1, 10), wcss_list)
  mtp.title('The Elobw Method Graph')
  mtp.xlabel('Number of clusters(k)')
  mtp.ylabel('wcss_list')
  mtp.show()

def KMEAN(n,arr):

  kmeans = KMeans(n_clusters=n, init='k-means++', random_state= 42)
  cluster=[[],[],[]]
  y_predict= kmeans.fit_predict(arr)
  centroids  = kmeans.cluster_centers_
  for i in range(0,len(arr)):
    if y_predict[i]==0:
      cluster[0].append(i)
    elif y_predict[i]==1:
      cluster[1].append(i)
    else:
      cluster[2].append(i)

  return [cluster,centroids]

def cal_cen(cluster1,cluster2,arr):
  sum1=0
  sum2=0


  for i in cluster1:
    sum1+=arr[i][0]
    sum2+=arr[i][1]

  for i in cluster2:
    sum1+=arr[i][0]
    sum2+=arr[i][1]

  centroid=[ sum1/(len(cluster1)+len(cluster2)),sum2/(len(cluster1)+len(cluster2)) ]

  return centroid

def KMEAN8(cluster,arr,centroid):
  n=8

  final_sub_clusters=[]

  for i in range(0,len(cluster)):
    temp=[]
    for j in cluster[i]:
      temp.append([arr[j][0],arr[j][1]])
    if len(cluster[i])>=8:
      kmeans = KMeans(n_clusters=8, init='k-means++', random_state= 42)
    elif len(cluster[i])>=4:
      n=4
      kmeans = KMeans(n_clusters=4, init='k-means++', random_state= 42)
    else:

      final_sub_clusters.append(cluster[i])
      continue
    y_predict= kmeans.fit_predict(temp)
    sub_centroids  = kmeans.cluster_centers_
    sub_clusters=[[],[],[],[],[],[],[],[]]

    for j in range(0,len(cluster[i])):
      sub_clusters[y_predict[j]].append(cluster[i][j])


    ans=[]

    for j in range(0,n):
      merged=[]
      for k in range(0,len(ans)):
        dis_centroid= math.sqrt((sub_centroids[j][0]-centroid[i][0])**2 + (sub_centroids[j][1]-centroid[i][1])**2)

        dis_sub_centroid= math.sqrt((sub_centroids[j][0]-ans[k][0])**2 + (sub_centroids[j][1]-ans[k][1])**2)

        if dis_sub_centroid<dis_centroid or len(sub_clusters[j])==1:
          t=cal_cen(sub_clusters[j],sub_clusters[ans[k][2]],arr)
          merged.append([t[0],t[1],ans[k][2],k])

      if len(merged)==0:
        ans.append([sub_centroids[j][0],sub_centroids[j][1],j,len(ans)])
      else:
        tx=min(merged)
        for jk in sub_clusters[j]:
          sub_clusters[tx[2]].append(jk)
        sub_clusters[j]=[]
        ans[tx[3]]=tx

    for j in range(0,len(sub_clusters)):
      if len(sub_clusters[j])==0 and len(arr)>=6:
        continue
      else:
        temp=[]
        for k in sub_clusters[j]:
          temp.append(k)
        final_sub_clusters.append(temp)


  return final_sub_clusters

def HEAD(cluster,coordinates,threshold):
  cluster_head=[-1 for j in range(0,len(cluster))]

  for i in range(0,len(cluster)):
    mini=1000000
    for j in range(0,len(cluster[i])):

      # for atleast 1 round => 90dbm, data, number of nodes in cluster, and other losses
      if (Energy[cluster[i][j]]-(10**4 * (len(cluster[i])-1) * 10**(-7) ) ) < threshold:
        continue
      t=0
      for k in range(j+1,len(cluster[i])):
        t+= math.sqrt( (coordinates[cluster[i][j] ][0]-coordinates[cluster[i][k]][0])**2 + (coordinates[cluster[i][j]][1]-coordinates[cluster[i][k]][1])**2)
      if(mini>t):
        mini=min(mini,t)
        cluster_head[i]=cluster[i][j]

  return cluster_head

def ROUNDS(cluster_head,threshold,Energy,cluster):
  mini=1000000
  for i in range(0,len(cluster_head)):
    if len(cluster[i])==1:
      mini=min(Energy[cluster_head[i]]//((10**(-9) )),mini)
      continue
    mini=min( (Energy[cluster_head[i]]-threshold)//(10**4 * (len(cluster[i])-1) * 10**(-7) ), mini)
  if mini<0:
    mini=0
  return int(mini)

def CHECK(threshold,cluster,coordinates,Energy):

  t=[0 for i in range(0, len(cluster))]
  update=False

  for i in range(0,len(cluster)):
    for j in cluster[i]:
      if (Energy[j]-( 100000 * (len(cluster[i])-1) * 0.0000001 )) >threshold:
        t[i]+=1
      if t[i]==1:
        break
    if t[i]==0:
      update=True
  #print(t)
  p=threshold

  if update==True:
    p-=0.01
  return p

def DEC_ENERGY(threshold,cluster,rounds,Energy,coordinates,cluster_head):
  cnt=False
  deadNodes=[]

  for num in range(0,rounds):
    for k in range(0,len(cluster)):
      cnt=0
      for i in cluster[k]:
        if(Energy[i]>10**4 * 10**(-7)):
          cnt+=1
      Energy[cluster_head[k]]-=(10**4 * cnt * 10**(-7) )

      for i in cluster[k]:
        distance= ( (coordinates[i][0]-coordinates[cluster_head[k]][0] )**2 + (coordinates[i][1]-coordinates[cluster_head[k]][1])**2 )
        if distance==0:
          continue
        else:
          Energy[i]-=(distance* 10**4 * 10**(-9))

        if Energy[i]<=(10**4 * 10**(-7)):
          deadNodes.append(i)

  temp=[]
  ene=[]

  for i in range(0,len(coordinates)):
    set=False
    for j in range(0,len(deadNodes)):
      if deadNodes[j]==i:
        set=True
    if set==False:
      temp.append(coordinates[i])
      ene.append(Energy[i])


  return [temp,ene]

threshold=1
alive=[]
r=[0]
r1=0
cluster=[]

for i in range(0,4000):

  if len(arr)<=3:
    break
  c=KMEAN(3,arr)
  cluster=c[0]
  centroid=c[1]

  cluster=KMEAN8(cluster,arr,centroid)

  while(True):
    t=CHECK(threshold,cluster,arr,Energy)
    if t<0:
      if len(arr)!=3:
        threshold=0
      break


    elif t==threshold:
      break
    else:
      threshold=t

  if len(arr)<=3:
    break
  # threshold=CHECK(threshold,cluster,arr,Energy)
  cluster_head=HEAD(cluster,arr,threshold)
  rounds=ROUNDS(cluster_head,threshold,Energy,cluster)
  r1+=rounds
  A=DEC_ENERGY(threshold,cluster,rounds,Energy,arr,cluster_head)
  arr=A[0]
  Energy=A[1]
  alive.append(len(arr))
  r.append(r[-1]+rounds)

  # print(cluster_head)
  # print(len(arr),rounds,threshold,Energy)

print(r1)
print(len(arr))
print(Energy)

print(threshold)
print(len(cluster))
# for i in (0,len(cluster)):
#   for j in cluster[i]:
#     print(j)
print(cluster)
print(arr)

from matplotlib import pyplot as plt

plt.scatter(alive,r[1:])
# plt.scatter(a,r[1:])
plt.ylabel("alive")
plt.xlabel('rounds')
# plt.scatter([i for i in alive], [i for i in r[1:]])
# plt.axis([0,10,0,10])
plt.show()
print(alive)
print(r)

for i in range(0,len(alive)):
  print(alive[i],r[i+1])