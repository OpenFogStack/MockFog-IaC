"""

"""

from os import chdir, getcwd
import time
wd=getcwd()
chdir(wd)
import requests
from network import createNetwork
import json

import testTools
import network.createNetwork as net


def getHostIP():
    f = open("../created/nodemanager_info.json")
    nmInfo = json.load(f)
    return nmInfo



headers = {"accept": "application/json","content-type":"application/json"}
hostIP = getHostIP()["IP"]
basePath = "http://" + hostIP + ":7474/webapi/"
webappURL = "http://" + hostIP
swaggerURL = "http://" + hostIP + ":8888"
controllerURI = "http://" + hostIP + ":5001"
cloudProvider = "os"
#headers = {"accept": "text/plain","content-type":"application/json"}


def getNodes(agentIPpath):
      with open(agentIPpath, 'r') as f:
         return json.load(f)


def createTestNet():
    # init Network
    network = createNetwork.createTestNetwork(basePath,headers)
    docID = network.createDoc("testDoc1")
    network.createNets(2)
    network.createNodesInNets(3)
    time.sleep(2)    
    network.buildNetwork(cloudProvider)
    return("docID: " + str(docID))

def buildNetwork(docID,cloud):
        # Create .yml configuration and execute with ansible
        print "Network is built..."
        r = requests.get(basePath + "doc/" + str(docID) + "/bootstrap/" + cloud)
        print(str(r.status_code) + " " + r.text)        
   
def connectSubnets(network):
    # connect Subnets
    for netFrom in network.subNetIDs:
        for netTo in network.subNetIDs:
            if (netFrom != netTo) : network.createEdge(netFrom,netTo)


def getAllDocs():
    ### get all docs
    r = requests.get(basePath + "doc/")
    print(r.status_code)
    print(r.text)
    return r

def getDocInfo(docID):
    xx = requests.get(basePath + "doc/" + str(docID)).json()
    str(xx["allNets"].keys()[0])
    return xx

def getNodeInfo(docID,nodeID):
    xx = requests.get(basePath + "doc/" + str(docID) + "/vertex/" + str(nodeID)).json()
    return xx

def setConfigFile():
### Config Endpoint        
    ymlPath = basePath + "yml-config/os"
    ymlData = json.dumps({
    "os_ssh_key_name": "*********",
    "external_network": "tu-internal",
    "mgmt_network_name": "mgmt",
    "auth_url": "***********",
    "username": "*********",
    "password": "********",
    "project_name": "MockFog"
    })
    r = requests.post(ymlPath,data = ymlData,headers = headers)
    r.status_code

def createEdge(docID,fromID,toID):
    ### create Edge
    
    edgePath = basePath + "doc/" + str(docID) + "/edge/" + str(fromID) +"/" + str(toID)
    r = requests.post(edgePath,headers = headers)
    r.text

def postTC():
   basePath = "http://10.200.1.83:5000/tc-config/"
   dstNet = "10.0.3.0/24"
   exampleData = {
                 "out_rate": "100mbps",
                 "in_rate": "100mbps",
                 "rules": [
                   {
                     "dst_net": dstNet,
                     "out_rate": "10mbps",
                     "delay": "10ms",
                     "dispersion": "10ms",
                     "loss": "0.1",
                     "corrupt": "0.1",
                     "duplicate": "0.1",
                     "reorder": "0.1"
                   }
                 ]
               }
   return requests.post(basePath,
                     json.dumps(exampleData),headers = headers)

def destroyNet(docID):
   
   r = requests.delete(basePath + "doc/"+ str(docID) +"/destroy/os")
   
   return r

def agentIPs():
   return requests.get("http://10.200.1.85:5001/getAgentIPs",headers=headers)

def checkAgentstuff():
   endpoints = testTools.Endpoints()
   headers = endpoints.getHeaders()
   agents = endpoints.agents
   return headers,agents

def checkStatus():
   
   msg = requests.get("http://10.200.1.85:7474/webapi/ansiblelog",headers=headers).text
   msg_old = msg
   print msg
   while True:
      
      msg = requests.get("http://10.200.1.85:7474/webapi/ansiblelog",headers=headers).text
      if msg_old != msg:
         print msg
      time.sleep(1)

def testServicesOnline():
    
    testURI(basePath + "docs","testNEO")        
    testURI(webappURL,"checkWebInterface")
    testURI(swaggerURL,"testSwagger")
    
    
    
def testURI(URI, testFN):
    print("testing " + URI)
    try:
        testFun = getattr(testfunctions, testFN)
        result = testFun(URI)
        printTestResults(result)
    except Exception, e:
        print("Failed to Connect to " + URI + ". Error: " + str(e))

def printTestResults(r):
    if (r.status_code == 200) or (r.status_code == 404):
        print("OK")
    else: print("Failed.Status Code: " + str(r.status_code) + " Response: " + str(r.text))