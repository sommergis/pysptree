from pySPTree import SPTree
spt = SPTree(0,0,True)

f = file('simple_MCFP.net','r')
input = f.read()

spt.LoadDMX(input)

spt.ShortestPathTree()

retList = spt.Predecessors()
print type(retList), retList

retList = spt.ArcPredecessors()
print type(retList), retList
