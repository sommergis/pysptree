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

from pySPTree import *
print "\npySPTree Version '%s' successfully imported." % version()
print "\ntest #1"
spt = SPTree()
print "SPTree Class successfully instantiated."
FILENAME = 'sample.dmx'
print "Loading network from DIMACS file %s.." % FILENAME
f = open(FILENAME,'r')
inputStr = f.read()
f.close()
spt.LoadDMX(inputStr)

print "Setting time.."
spt.SetMCFTime()
spt.SolveMCF()
if spt.MCFGetStatus() == 0:
    print "Optimal solution: %s" %spt.MCFGetFO()
    print "Time elapsed: %s sec " %(spt.TimeMCF())
else:
    print "Problem unfeasible!"
    print "Time elapsed: %s sec " %(spt.TimeMCF())

print "\nShowing functionality of pySPTree.."
showModuleFunctionality()
# This causes Python to crash sometimes!
#del spt

print "\ntest #2"
spt = SPTree()
print "SPTree Class successfully instantiated."
print "Reading sample data.."

'''
c Problem line (nodes, links)
p min 4 5
c
c Node descriptor lines (supply+ or demand-)
n 1 4
n 4 -4
c
c Arc descriptor lines (from, to, minflow, maxflow, cost)
a 1 2 0 4 2
a 1 3 0 2 2
a 2 3 0 2 1
a 2 4 0 3 3
a 3 4 0 5 1
'''

nmx     = 4
mmx     = 5
pn      = 4
pm      = 5
pU      = [4,2,2,3,5]
pC      = [2,2,1,3,1]
pDfct   = [-4,0,0,4]
pSn     = [1,1,2,2,3]
pEn     = [2,3,3,4,4]

spt.LoadNet(nmx, mmx, pn, pm, CreateDoubleArrayFromList(pU), CreateDoubleArrayFromList(pC),
            CreateDoubleArrayFromList(pDfct), CreateUIntArrayFromList(pSn),
            CreateUIntArrayFromList(pEn))

print "Setting time.."
spt.SetMCFTime()
spt.SolveMCF()
if spt.MCFGetStatus() == 0:
    print "Optimal solution: %s" %spt.MCFGetFO()
    print "Time elapsed: %s sec " %(spt.TimeMCF())
else:
    print "Problem unfeasible!"
    print "Time elapsed: %s sec " %(spt.TimeMCF())

print "\nShowing functionality of pySPTree.."
showModuleFunctionality();
del spt

