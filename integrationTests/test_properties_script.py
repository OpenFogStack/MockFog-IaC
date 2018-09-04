# -*- coding: utf-8 -*-
"""

"""

import testTools
import time
from pingAgent import Agent
import json

def createNet():
   tools = testTools.Tools()
   tools.createTestNet(2,1,"streight")
   time.sleep(1)
   tools.buildTestNet()
   tools.checkStatus()
   time.sleep(20)
   agents = Agent(tools.getAgents(),"shell")
   agents.addHostsToNodes()
   
   return tools, agents

def testDelay(agents, tools_):
   
   testDelay = 10
   
   network = tools_.Thenetwork
   
   testProp = json.dumps({"in_rate": "1000000",
                          "out_rate": "1000000",
                          "delay": str(testDelay),
                          "dispersion": "0",
                          "loss": "0.0",
                          "corrupt": "0.0",
                          "duplicate": "0.0",
                          "reorder": "0.0"})
   
   nodeIDs = network.nodeIDs
   testNodeID = nodeIDs[0]
   print str(testNodeID)
   testNodeName = tools_.getNodeInfo(testNodeID)[str(testNodeID)]["name"]
   print (testNodeName)
   targetNodeID = nodeIDs[1]
   targetNodeName = tools_.getNodeInfo(targetNodeID)[str(targetNodeID)]["name"]
   pingInfo = agents.pingTo(testNodeName,targetNodeName).json()
   init_delay = pingInfo[targetNodeName]["rtt_avg"]
   print "initial delay from " + testNodeName + " to " + targetNodeName \
         + ": " + str(init_delay)
   
   print "setting Delay = " + str(testDelay) + " seconds..."
   edge = network.getNodeEdge(testNodeID)
   network.putEdge(edge[0],edge[1],testProp)
   time.sleep(2)
   agents.addHostsToNodes()
   pingInfo = agents.pingTo(testNodeName,targetNodeName).json()
   delay = pingInfo[targetNodeName]["rtt_avg"]
   delta = float(delay) - float(init_delay)
   print "current delay from " + testNodeName + " to " + targetNodeName \
         + ": " + str(delay) + ". Delta = " + str(delta)
         
