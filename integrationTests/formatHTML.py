from requests import get



def printTableHeader():
    print formatOutput(["From","To","Results"],str(int(colWidth)*2)) +  "</br>"
    print formatOutput(["Name","IP","Name","IP","Packets","Received","Loss","Delay"],colWidth) +  "</br>"

def setHTMLheader():
   baseTableColWidth = 120
   tabHeader1Width = baseTableColWidth * 2
   
   #ip = get('https://api.ipify.org').text
   #print "<head><link rel=\"stylesheet\" type=\"text/css\" href=\"http://" + ip +  "/css/outputPingtest.css\"></head>"
   print "<head><style> \
      .addHosts {width: 300px;display:inline-block;} \
      .headline1 {font-size:14pt;margin-top:30px;display:block;} \
      .tabHeader1 {width: " + str(tabHeader1Width) + "px;display:inline-block;} \
      .tabHeader2 {width: " + str(baseTableColWidth) + "px;display:inline-block;} \
      .tabCol {width: " + str(baseTableColWidth) + "px;display:inline-block;} \
      .error {width:100%} \
      </style></head>"
        
def printHTML(msg,htmlClass,newLine):
   msg = "<span class = \"" + htmlClass + "\">" + str(msg) + "</span>"
   if newLine: msg = msg + "</br>"
   print msg
   
def printPingTable(style,values,newLine = True):
   if style == "header1": printTabVals(values,"tabHeader1")
   elif style == "header2": printTabVals(values,"tabHeader2")
   elif style == "row": printTabVals(values,"tabCol")
   elif style == "headline": printTabVals(values,"headline1")
   elif style == "error": printTabVals(values,"error")
   if newLine: print "</br>"

def printTabVals(values,htmlClass):
   outHTML = ""
   span = "<span class = \"" + htmlClass + "\">"
   for value in values:         
      outHTML = outHTML + span + str(value) + "</span>"
   print outHTML
   