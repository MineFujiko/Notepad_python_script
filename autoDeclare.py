#auto port declare
from Npp import *
import re

#debug print
def testPrint(str):
    console.show()
    console.write(str + "\n")
    return

def getPortPara(portStr):
    portNameRe = re.search(r'(\w+)',portStr)
    portName = portNameRe.group(0)
    portWidthRe = re.search(r'\[\s*(\d+)',portStr)
    portWidth = portWidthRe.group(0)
    return portName,portWidth

def getAllLines(startLineNum,endLineNum):
    allLinesList = []
    for i in range(startLineNum,endLineNum+1):
        singleLine = editor.getLine(i)
        allLinesList.append(singleLine)
    return allLinesList

def getDeclarePos(allLineInlist):
    """Get the position of variate declared"""
    tagFlagCnt = 0
    lineNumLocked = 0
    for i in range(len(allLineInlist)):
        #remove 
        lineStr = allLineInlist[i].strip()
        #search the tag
        tagFlag = re.search(r'///The End of Declare',lineStr)
        if tagFlag == None :
            tagFlagCnt = tagFlagCnt + 0
        else:
            tagFlagCnt = tagFlagCnt + 1
            lineNumLocked = i
        break
    
    #Warning judge
    if tagFlagCnt == 0:
        notepad.messageBox('There is no tag for port declare!!\nPlease add the tag"///The End of Declare"','WARNING!')
    
    return lineNumLocked


def autoDeclare():
    """port autodeclare"""
    #Get port name and port list
    portStr = editor.getSelText()
    [portName,portWidth] = getPortPara(portStr)

    #Get all text in list
    editor.selectAll()
    lineSelection = editor.getUserLineSelection()
    startLineNum = lineSelection[0]
    endLineNum = lineSelection[1]
    allLineInlist = getAllLines(startLineNum,endLineNum)
    #Get the position of variate declared
    declarePos = getDeclarePos(allLineInlist)

    #INSERT THE PORT DELARATION
    if portWidth == '':
        portDelaration = 'reg' + ' '*4 + portName + ';'
    else:
        portDelaration = 'reg' +  ' '*4 + '[' + portWidth + ' :0]' + portName + ';'
    editor.gotoLine(declarePos)
    editor.newLine()
    editor.replaceLine(declarePos-1,portDelaration)
    
#MAIN FUNCTION
if __name__ == '__main__':
    autoDeclare()
