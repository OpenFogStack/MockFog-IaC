"""
@author: miconzelmann
"""

import json
import requests
import sys
import formatHTML

class Agent():
# Provides functionality to communicate and make tests on created nodes """
   
   def __init__(self, nodes, outputMode="html"):
      """ nodes: json containing information about created nodes.
                eg. from Nodemanager : /opt/Mockfog/iac/created/agentIPs.json
                or via ENdpoint: <nodemanagerIP>:5001/getAgentIPs
      """
      self.headers = {"accept":"application/json","content-type":"application/json"}
      self.nodes = nodes
      self.outputMode = outputMode
    			
   def addHostsToNodes(self):
      # Adds Hosts in Network to the List of known hosts in each node
      # INPUT: 
      #         nodes: json() object   created from <Path/to/iac/Repo>/created/agentIPS.json
      self.printOutput("Adding created nodes to each nodes' known-hosts...",True,htmlClass = "headline1")
      
      for srcNodeName in self.nodes.keys():        
         srcIP = self.nodes[srcNodeName]["public_addr"]
         #srcIP = self.nodes[srcNodeName]["mgmt"]["addr"]
         pingURI = "http://" + srcIP + ":5000/api/ping"
         sys.stdout.flush()
         self.printOutput("Adding hosts To " + srcNodeName + "(" + srcIP + ")...",False,htmlClass = "addHosts")
         requestData = json.dumps({"threads_num": 1,"seconds": "1","hosts": self.createHostsList(srcNodeName,"json")})
         try: 
            r = requests.post(pingURI,data=requestData,headers=self.headers,timeout=0.5)
            if r.status_code == 200: self.printOutput("OK.",True,"addHosts")
            else: self.printOutput("Failed with " + str(r.status_code) + ". Response: " + r.text,True,"addHosts")
         except Exception, e:
            self.printOutput("Failed to Connect to " + pingURI + str(e)[0:50],True,htmlClass = "addHosts")
      
   def printOutput(self,msg,newLine,htmlClass = "addHosts"):
      if self.outputMode == "html":         
         formatHTML.printHTML(msg,htmlClass,newLine)
      elif self.outputMode == "shell": 
         if newLine: print msg, 
         else: print msg
   
   def createHostsList(self,srcNodeName,mode):
      #creates List of nodes not equal to srcNode 
      hosts = []
      for dstNodeName in self.nodes.keys():       
         if srcNodeName != dstNodeName:         
            #dstIP = self.nodes[dstNodeName]["public_addr"]      
            #dstIP = self.nodes[dstNodeName]["mgmt"]["addr"]
            dstIP = self.getLocalIP(self.nodes[dstNodeName])
            if mode == "json": hosts.append({"hostname":dstNodeName,"ip":dstIP})
            elif mode == "list": hosts.append(dstNodeName)
      return hosts
   
   def getLocalIP(self,nodeDict):
      for key in nodeDict.keys():
         if (key != "public_addr" and key != "mgmt"):
            return nodeDict[key]["addr"]
   
   def pingTo(self,fromNode,toNode):
      srcIP = self.nodes[fromNode]["public_addr"]
      #srcIP = self.nodes[fromNode]["mgmt"]["addr"]
      pingURI = "http://" + srcIP + ":5000/api/ping/"
      return requests.get(pingURI + str(toNode),timeout=1)
    
   def pingAllToAll(self):
      for nodeName in self.nodes:
         srcIP = self.nodes[nodeName]["public_addr"]
         #srcIP = self.nodes[nodeName]["mgmt"]["addr"]
         pingURI = "http://" + srcIP + ":5000/api/ping/"
         for dstName in self.createHostsList(nodeName,"list"): 
            self.printIPRequest(requests.get(pingURI + dstName,timeout=0.5))
   
   def printIPRequest(self,requestObj):
      sys.stdout.flush()
      print self.printOutput(requestObj.text,"shell",True)
      

