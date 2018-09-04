# -*- coding: utf-8 -*-
"""
Created on Sat Aug 04 08:28:21 2018

"""

import json
import requests
import time
from network.createNetwork import createTestNetwork

class Tools():
   """ Tools to get Information about and communicate with 
       the Nodemanger and Agents"""
   
   hostIP = ""
   agents = {}
   currentDocID = -1
   
   T_BOOTSTRAP_PER_NODE = 150          #sec
   T_BOOTSTRAP_PER_NETWORK = 60        #sec
   T_MAX_BOOTSTRAP = 0
   T_MAX_DESTROY = 300
   T_DESTROY_NET = 10   # Time to destroy one subnet
   ############## CREDENTIALS ############
   OPENSTACK_CRED = json.dumps({
    "ssh_key_name": "mockfog",
    "external_network": "tu-internal",
    "auth_url": "http://cloud.cit.tu-berlin.de:5000/v2.0",
    "username": "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "password": "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "project_name": "MockFog"
    })
   
   
   def __init__(self):
      
      self.setHostIP()
      self.setEndpoints()
      self.getAgents()
      #self.swaggerData = json.load(open("swagger.json"))
      self.loadSwaggerInfo("nm")
      self.setOSConfig()
      
   def setOSConfig(self):
      try:
         r = requests.post(self.basePath + "yml-config/os",
                        data = self.OPENSTACK_CRED,
                        headers = self.headers)
         if r.status_code == 200: 
            print "setting Credentials successful."
         else: 
            print "setting Credentials failed. Errorcode: " + str(r.status_code) \
                  + " Message: " + str(r.text)
      except Exception:
         print "could not set credentials: connection failed."
      
   
   def setHostIP(self):
      path_ = "../created/nodemanager_info.json"
      try:
         f = open(path_)
         nmInfo = json.load(f)
         self.hostIP = nmInfo["IP"]
      except Exception:
         print("could not load nodemanager IP")
         self.hostIP = raw_input("please insert IP:")
         json.dump({"IP": self.hostIP}, open(path_,"w"))
         print("nodemanager IP saved to : " + path_)
   
   def setEndpoints(self):
      self.headers = {"accept": "application/json","content-type":"application/json"}      
      #headers = {"accept": "text/plain","content-type":"application/json"}
      self.basePath = "http://" + self.hostIP + ":7474/webapi/"
      self.webappURL = "http://" + self.hostIP
      self.swaggerURL = "http://" + self.hostIP + ":8888/"
      self.controllerURI = "http://" + self.hostIP + ":5001/"
   
   def loadSwaggerInfo(self,mode):
      try:
          if mode == "nm":
             r = self.getRequest(self.swaggerURL + "swagger.json")
             self.nmSwaggerData = r.json()
          elif mode == "agent":
             r = self.getRequest("http://" + self.getAgentIP() + ":5000/api/" \
                              + "swagger.json")
             self.agentSwagger = r.json()
      except Exception, e:
          print("could not retreive swagger info for " + mode + ". Error: " + str(e.message))
          
      return r.json()
   
   def getRequest(self,URI):
      tries = 0
      while tries < 3:
         try:
            return requests.get(URI,headers=self.headers)
         except Exception,e:
            time.sleep(1)
            tries += 1
      print "could not establish connection to " + URI \
            + " Error: " + str(e.message)
      return None
   
   def getAgentIP(self):
      nodeName = self.agents.keys()[0]
      return self.agents[nodeName]["public_addr"]
  
   def getAgents(self):
      if self.hostIP == "": self.setHostIP()
      self.agents = self.getRequest("http://" + self.hostIP \
                                    + ":5001/getAgentIPs").json()
      return self.agents
   
   def getNodeInfo(self,nodeID):
      return self.getRequest(self.basePath + "doc/" + str(self.currentDocID) \
                           + "/vertex/" + str(nodeID)).json()
   
   
   
   def getHeaders(self):
      return self.headers
   
   def getBasepath(self):
      return self.basePath
   
   def getSwaggerData(self,path,mode = "postExample",getAll = False):
      """ returns example Data from swagger documentation for POST requests.
          path:   URI for which the sample Data should be retreived:
                  Example:"/doc/{docId}/node" get POS
      """
      postData = {}
      if mode == "postExample":         
         for prop in self.nmSwaggerData["paths"][path]["post"]["parameters"][1]["schema"]["properties"]:
            propData = self.nmSwaggerData["paths"][path]["post"]["parameters"][1]["schema"]["properties"][prop]
            if propData.has_key("enum"): 
               if getAll: exVal = propData["enum"]
               else: exVal = propData["enum"][0]
            else: exVal = propData["example"]
            postData.update({prop:exVal})
      return postData

   def checkAnsible(self):
      msg = self.getRequest(self.basePath + "ansiblelog").json()["msg"]
      return msg
   
   def checkStatus(self):
      print "checking status on network instantiation..."
      msg = self.checkAnsible()

      if msg == "Document not instantiated.":
         return False,"Bootstrapping of Network not started"
      print "Max. Time Estimated: " + str(self.T_MAX_BOOTSTRAP) + " seconds..."
      t = 0
      while msg != "Bootstrapping done." and int(t)<int(self.T_MAX_BOOTSTRAP):
         time.sleep(10)
         msg = self.checkAnsible()
         t += 10
         print "T: " + str(t) + "sec. Status: " + msg.replace("\n",".")
         
      if msg == "Bootstrapping done.": 
         print msg
         print "checking if agents created..."
         time.sleep(5)
         self.getAgents()
         if self.checkNodesAlive():
            return True,"Bootstrapping done."
         else: 
            return False,"Cant reach agents. Network not created..."
      else:
         return False,"Timelimit reached. Network not created..."
      
   def checkNodesAlive(self):
      print "checking if nodes are alive...",
      for node in self.agents.keys():
         ip = self.agents[node]["public_addr"]
         print ip,
         if not self.testConnection("http://" + ip \
                                   + ":5000/api/" + "swagger.json"):
            print "failed."
            return False
         print "ok",
      print "done."
      return True
      
   
   def checkNodesDead(self):
      print "checking if nodes are dead...",
      for node in self.agents.keys():
         ip = self.agents[node]["public_addr"]
         print ip + ",",
         if self.testConnection("http://" + ip + ":5000/api/" + "swagger.json"):
            return False
            print "failed."
         else: print "ok.",
      print "done."
      return True
   
   def testConnection(self,URI):
      try:
         r = requests.get(URI,headers=self.headers)
         if r.status_code == 200: 
            return True
         else:
            return False
      except Exception:
         return False
      
   def createTestNet(self,nets,nodes,mode):
      # init Network
      print("create Network with " + str(nets) + " subnetworks and " \
            + str(nodes) + " Nodes in subnets with mode: " + mode +"...")
      self.nNets = nets
      self.nNodes = nodes
      self.netMode = mode
      self.Thenetwork = createTestNetwork(self.basePath,self.headers)

      time.sleep(1)
      self.currentDocID = self.Thenetwork.createDoc("FullyConNet4")
      self.Thenetwork.createNets(nets)
      self.Thenetwork.createNodesInNets(nodes)
      self.Thenetwork.connectNets(mode)
      
      # calc maximum estimated time to bootstrap
      self.T_MAX_BOOTSTRAP = 500 + nodes * nets * self.T_BOOTSTRAP_PER_NODE
      
   def buildTestNet(self):
      print "building network with docID " + str(self.currentDocID)
      return self.Thenetwork.buildNetwork("os")
      
   def destroyNet(self):
      print "destroying network with docID " + str(self.currentDocID)
      time.sleep(1)
      self.Thenetwork.destroyNetwork()
      t = 0
      while not self.checkNodesDead() and t<self.T_MAX_DESTROY:
         time.sleep(10)
         t += 10
         print "Time elapsed: " + str(t)  + " seconds."
      
      if t>self.T_MAX_DESTROY: 
         return False
      else:
         t_down = self.nNets * self.T_DESTROY_NET
         print "nodes successfully destroyed. Waiting for networks... "
         print "Estimated time: " + str(t_down) + " seconds."
         time.sleep(t_down)
         return True
   
   def deleteDoc(self):
      r = requests.delete(self.basePath + "doc/" + str(self.currentDocID))
      if r.status_code == 200: self.currentDocID = -1
      return r
      
