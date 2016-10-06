'''
 ####################################################################################
 * Linear and Quadratic Min Cost Flow problems solver based on the (primal and
 * dual) simplex algorithm. Conforms to the standard MCF interface defined in
 * MCFClass.h.
 *
 * Version 1.00
 *
 * date 29 - 08 - 2011
 *
 * author Alessandro Bertolini \n
 *         Antonio Frangioni \n
 *         Operations Research Group \n
 *         Dipartimento di Informatica \n
 *         Universita' di Pisa \n
 *
 * Copyright &copy 2008 - 2011 by Alessandro Bertolini, Antonio Frangioni
 *
 * Made available through SWIG: 
 * 		Johannes Sommer, 2013
 *		G#.Blog
 *		www.sommer-forst/blog
 ####################################################################################
 *
 *		Sample script for pySPTree
 *
 ####################################################################################'''

ALLDEST     = True
UINT_MAX    = 4294967295
DIRECTED    = True

def showModuleFunctionality():
	nmx     = spt.MCFnmax()
	mmx     = spt.MCFmmax()
	pn      = spt.MCFnmax()
	pm      = spt.MCFmmax()

	pU      = []
	caps = new_darray(mmx)
	spt.MCFUCaps(caps)
	for i in range(0,mmx):
		pU.append(darray_get(caps,i))

	pC      = []
	costs = new_darray(mmx)
	spt.MCFCosts(costs)
	for i in range(0,mmx):
		pC.append(darray_get(costs,i))

	pDfct   = []
	supply = new_darray(nmx)
	spt.MCFDfcts(supply)
	for i in range(0,nmx):
		pDfct.append(darray_get(supply,i))

	pSn     = []
	pEn     = []
	startNodes = new_uiarray(mmx)
	endNodes = new_uiarray(mmx)
	spt.MCFArcs(startNodes,endNodes)
	for i in range(0,mmx):
		pSn.append(uiarray_get(startNodes,i)+1)
		pEn.append(uiarray_get(endNodes,i)+1)

	print "arc flow"
	length = spt.MCFm()
	flow = new_darray(length)
	length = spt.MCFn()
	nms = new_uiarray(length)
	spt.MCFGetX(flow,nms)
	for i in range(0,length):
	   print "flow",darray_get(flow,i),"arc",uiarray_get(nms,i)
	   
	print "node potentials"
	length = spt.MCFn()
	costs = new_darray(length)
	spt.MCFGetPi(costs,nms)
	for i in range(0,length):
	   print "flow",darray_get(costs,i),"node",i+1

	print "reading graph - arcs"
	length = spt.MCFm()
	startNodes = new_uiarray(length)
	endNodes = new_uiarray(length)
	spt.MCFArcs(startNodes,endNodes)
	for i in range(0,length):
	   print "Arc %s: start %s end %s" % (i, uiarray_get(startNodes,i)+1,uiarray_get(endNodes,i)+1)

	print "reading graph - costs"
	length = spt.MCFm()
	costs = new_darray(length)
	spt.MCFCosts(costs)
	for i in range(0,length):
	   print "Arc %s: cost %s" % (i, darray_get(costs,i))

	print "reading graph - capacities"
	length = spt.MCFm()
	caps = new_darray(length)
	spt.MCFUCaps(caps)
	for i in range(0,length):
	   print "Arc %s: capacities %s" % (i, darray_get(caps,i))

	print "reading nodes - supply/demand"
	length = spt.MCFn()
	supply = new_darray(length)
	spt.MCFDfcts(supply)
	for i in range(0,length):
	   print "Node %s: demand %s" % (i+1, darray_get(supply,i))


# def buildSPTree(origin, spt, printOutput ):
    # '''Build Shortest Path Tree from 1 Origin to all Dests '''
    # arcPre = spt.ArcPredecessors()
    # pre = spt.Predecessors()
    # print "arcPre"
    # print arcPre
    # print "pre"
    # print pre
    # #print arcPre, pre
    # counter = 0
    # lastStartNode = UINT_MAX
    # lastEndNode = UINT_MAX
    # setLastNodes = True
    # startNodeVisited = False
    # startNode = -1
    # endNode = -1
    # length = spt.MCFnmax() + 1
    # for i in range(1,length):
        # #print i
        # if arcPre[i] != UINT_MAX:
            # arcIndex = arcPre[i]
            # startNode = pre[i]
            # endNode = i
            # if printOutput:
                # print "  Solution Arc: #" , arcIndex , " (" , startNode , "," , endNode , ")"
    # counter = counter +1
    # return counter

def buildODPath(origin, dest, arcPredList, printOutput ):
    '''Build Shortest Path Tree from 1 Origin to 1 Dest '''
    output = {}

    #print UINT_MAX
    counter = 0
    lastStartNode = UINT_MAX
    lastEndNode = UINT_MAX
    setLastNodes = True
    endNodeReached = False
    startNodeReached = False
    arcsList = []
    for arcPred in arcPredList:
        startNode = arcPred[0]
        endNode = arcPred[1]
        # Search for arc with the endNode as toNode
        if endNode == dest:
            endNodeReached = True
        if endNodeReached:
            if lastStartNode != UINT_MAX and lastEndNode != UINT_MAX:   
                #print "s,e:",startNode, endNode
                if endNode == lastStartNode:
                    arcsList.append( (startNode,endNode) )
                    if printOutput:
                        print "  Solution Arc: (" , startNode , "," , endNode , ")"
                    counter = counter +1
                    setLastNodes = True
                #don't set lastStartNode if endNode != lastStartNode
                else:
                    setLastNodes = False
                if startNode == origin and endNode == lastStartNode:
                    break
            #first output
            elif lastStartNode == UINT_MAX and lastEndNode == UINT_MAX:
                arcsList.append( (startNode,endNode) )
                counter = counter +1
                if printOutput:
                    print "First Arc"
                    print "  Solution Arc: (" ,startNode ,"," , endNode , ")"
            if setLastNodes:
                lastEndNode = endNode
                lastStartNode = startNode
    output["arcs"] = arcsList
    output["count"] = counter
    #output["arcPreList"] = arcPreList
    #output["predecList"] = predecList
    return output


def getArcPredecessors(spt):
    output = {}
    arcPre = spt.ArcPredecessors()
    pre = spt.Predecessors()
    arcPredList = []
    predList = []
    length = spt.MCFnmax()
    for i in range(length,0,-1):
        if arcPre[i] != UINT_MAX:
            arcIndex = arcPre[i]
            startNode = pre[i]
            endNode = i
            arcPredList.append( (startNode,endNode ))
            predList.append(startNode)
    output["arcPredList"] = arcPredList
    output["predList"] = predList
    return output



from pySPTree import *
import sys
print "\npySPTree Version '%s' successfully imported." % version()
print "\ntest #1"
spt = SPTree(0,0,DIRECTED)
print "SPTree Class successfully instantiated."
#FILENAME = 'simple_MCFP.net' 
FILENAME = sys.argv[1] #'../../network_flow/netgen_instances/big8.net'
print "Loading network from DIMACS file %s.." % FILENAME
f = open(FILENAME,'r')
inputStr = f.read()
f.close()

alg = ''
if SPT_ALGRTM == 0:
    alg = "LQueue"
elif SPT_ALGRTM == 1:
    alg = "LDeque"
elif SPT_ALGRTM == 3:
    alg = "Dijkstra"
elif SPT_ALGRTM == 4:
    alg = "Heap"
    
print "ALGORITHM:", alg
try:
    spt.LoadDMX(inputStr)
except Exception, ex:
    raise RuntimeError("%s" %ex)

print "Setting time.."
spt.SetMCFTime()

if ALLDEST == True:
    dest = UINT_MAX

for i in range(0,spt.MCFn()):
    if spt.MCFDfct(i) < 0:
        origin = i + 1
    elif spt.MCFDfct(i) > 0:
        dest = i + 1
        
#origin = 63
#dest = 52

spt.SetOrigin(origin)
spt.SetDest(dest)

print " Origin: ", origin
if ALLDEST == False:
    print " Destination: " , dest
else:
    print " Destination: all nodes"

spt.ShortestPathTree()

if dest != UINT_MAX and spt.Reached(dest)== False:
    raise RuntimeError("Destination not reachable!")

print "Shortest Path Tree - rooted at: " , origin

counter = 0
if ALLDEST:
    if DIRECTED:
        # expensive method call!
        preDict = getArcPredecessors(spt)
        for nodeName in range(1,spt.MCFn()+1,1):
            if origin != nodeName:
                outDict = buildODPath(origin, nodeName, 
                                        sorted(preDict.get("arcPredList"),
                                        reverse=True, key=lambda x: x[0]), 
                                        False)
                if outDict.get("count") > 0:
                    counter = counter + outDict.get("count")
                    print "origin: %s dest:%s" % (origin, nodeName)
                    for arc in outDict.get("arcs"):
                        print arc
    else:
        # TODO
        preDict = getArcPredecessors(spt)
        for nodeName in range(1,spt.MCFn()+1,1):
            if origin != nodeName:
                outDict = buildODPath(origin, nodeName, 
                                        sorted(preDict.get("arcPredList"),
                                        reverse=True, key=lambda x: x[0]), 
                                        False)
                if outDict.get("count") > 0:
                    print "origin: %s dest:%s" % (origin, nodeName)
                    for arc in outDict.get("arcs"):
                        print arc
else:
    preDict = getArcPredecessors(spt)
    # sorts by second column in tuple
    outDict = buildODPath(origin, dest, 
                            sorted(preDict.get("arcPredList"),
                            reverse=True, key=lambda x: x[0]), True)
##    print "arcPreList"
##    for arc in sorted(preDict.get("arcPredList"), 
##                        reverse=True, key=lambda x: x[0]):
##        print arc
##    print "end"
##    print "predecList"
##    for pre in preDict.get("predList"):
##        print pre
##    print "end"
    for arc in outDict.get("arcs"):
        print arc
        
print "  Node count: #" , spt.MCFn()
print "  Arc count: #" ,spt.MCFm()
print "  Arc count of SPT: #" , counter
#print "Dests", spt.Dests()
'''
if spt.MCFGetStatus() == 0:
    print "Optimal solution: %s" %spt.MCFGetFO()
    print "Time elapsed: %s sec " %(spt.TimeMCF())
else:
    print "Problem unfeasible!"
    print "Time elapsed: %s sec " %(spt.TimeMCF())
'''

#print "\nShowing functionality of pySPTree.."
#showModuleFunctionality();
del spt