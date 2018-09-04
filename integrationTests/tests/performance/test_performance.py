# -*- coding: utf-8 -*-
"""

"""

import testTools
import time
from pingAgent import Agent
import json
import pandas
import matplotlib.pyplot as plt

def createNet(nets,nodes):
   tstart_rollout = time.time()
   tools = testTools.Tools()
   tools.createTestNet(nets,nodes,"streight")
   time.sleep(1)
   tools.buildTestNet()
   done, msg = tools.checkStatus()
   print msg
   if done:
      t_end_rollout = time.time()
   else: 
      t_end_rollout = 0
   t_rollout = t_end_rollout - tstart_rollout
   time.sleep(10)
   tstart_destroy = time.time()

   tools.destroyNet()
   t_end_destroy = time.time()
   t_destroy = t_end_destroy - tstart_destroy
   return t_rollout, t_destroy

def formatResults(allnets,allnodes,t_perform):
   data = pandas.DataFrame(columns=["nets","nodes","t_build","t_destroy"])
   for i in range(len(allnets)):
      data.loc[i+1]=[int(allnets[i]),
              int(allnodes[i]),
              t_perform[i][0],
              t_perform[i][1]]
   return data

def loadData(path_):
   return pandas.read_csv(path_)

def plotResults(data,mode="single"):
   
   
   #plot the results
   if mode == "single":
      # single network with increasing number of nodes
      
      plt.figure(1)
      singleNet = data.loc[(data.nets == 1) & (data.t_build > 0)]
      plt.scatter(singleNet.nodes, singleNet.t_build,marker="o")
      plt.scatter(singleNet.nodes, singleNet.t_destroy,marker="x")
      plt.xticks(range(1,int(max(singleNet.nodes))))
      plt.xlabel("number of created nodes")
      plt.ylabel("t[ms]")
      plt.title("nodes created in single network")
      plt.legend()
      plt.savefig("performance_singlenet.jpg")
   elif mode == "multi":
      # multibple networks with one node per network
      
      plt.figure(2)
      multiNet = data.loc[(data.nodes == 1) & (data.t_build > 0)]
      plt.scatter(multiNet.nets, multiNet.t_build,marker="o")
      plt.scatter(multiNet.nets, multiNet.t_destroy,marker="x")
      plt.xticks(range(1,int(max(multiNet.nets))))
      plt.xlabel("number of created nets")
      plt.ylabel("t[ms]")
      plt.title("one node per network")
      plt.legend()
      plt.savefig("performance_multinet.jpg")
      
   
def runTest():
   t_perform = []
   allnodes = []
   allnets = []
   
   # test single network with increasing number of nodes
   for nodes in range(1,5):
      nets = 1
      t_perform.append(createNet(nets,nodes))
      allnodes.append(nodes)
      allnets.append(nets)
      
   # test multiple networks with 1 node per network
   for nets in range(1,5):
      nodes = 1
      t_perform.append(createNet(nets,nodes))
      allnodes.append(nodes)
      allnets.append(nets)
   
   
   # test combinations of nodes and networks
   for nets in range(2,4):
      for nodes in range(1,2):
         nodes = 1
         t_perform.append(createNet(nets,nodes))
         allnodes.append(nodes)
         allnets.append(nets)
         
   for nodes in range(1,4):
      nets = 2
      t_perform.append(createNet(nets,nodes))
      allnodes.append(nodes)
      allnets.append(nets)

   # save results
   dataOut = formatResults(allnets,allnodes,t_perform)
   fOut = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".csv"
   dataOut.to_csv("results/" + fOut, index=False)

   
#
#t_perform = []
#allnodes = []
#allnets = []

# test single network with increasing number of nodes
#for nets in range(6,11):
#   nodes = 1
#   t_perform.append(createNet(nets,nodes))
#   allnodes.append(nodes)
#   allnets.append(nets)

#for nodes in range(1,9):
#   nets = 1
#   t_perform.append(createNet(nets,nodes))
#   allnodes.append(nodes)
#   allnets.append(nets)
#
#for nets in range(2,5):
#      for nodes in range(2,4):
#         nodes = 1
#         t_perform.append(createNet(nets,nodes))
#         allnodes.append(nodes)
#         allnets.append(nets)
#         
## save results
#dataOut = formatResults(allnets,allnodes,t_perform)
#fOut = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".csv"
#dataOut.to_csv("tests/performance/results/" + fOut, index=False)
#   json.dump(t_perform,open("resultsPerformance.json","w"))
#   json.dump(t_perform,open("resultsPerformanceNumberOfNodes.json","w"))
#   json.dump(allnodes,open("resultsPerformanceNumberOfNodes.json","w"))
#   json.dump(allnets,open("resultsPerformanceNumberOfNets.json","w"))
   
