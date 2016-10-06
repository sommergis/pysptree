# pysptree
Python Wrapper for SPTree - efficient solving of shortest path problems

## 1. What?
pySPTree is a Python-Wrapper for the C++ SPTree Solver Class from the Operations Research Group at the University of Pisa:

http://www.di.unipi.it/optimize/Software/MCF.html#SPTree

SPTree is a Class that solves special variations of Minimum Cost Flow Problems which are in fact shortest path (tree) problems (1 source node, 1 to n sink nodes, uncapacited arcs) very fast.

## 2. How?
pySPTree was being made available through SWIG.

## 3. Who?
The author of SPTree is Antonio Frangioni from the Operations Research Group at the Dipartimento di Informatica of the University of Pisa.

pySPTree is brought to you by Johannes from the G#.Blog

    http://www.sommer-forst.de/blog.

Feel free to contact me: info(at)sommer-forst.de

## 4. Quick start
Loading a Minimum Cost Flow Problem instance from DIMACS format and solve it

Here is a first start. "sample.dmx" must be in the same location of your python script. With these lines of code you can parse a minimum cost flow problem in DIMACS file format and solve it.

```
from pySPTree import * 
print "pySPTree Version '%s' successfully imported." % version() 
spt = SPTree() print "SPTree Class successfully instantiated." 

FILENAME = 'sample.dmx' 
print "Loading network from DIMACS file %s.." % FILENAME 
f = open(FILENAME,'r') inputStr = f.read() 
f.close() 

spt.LoadDMX(inputStr)

print "Setting time.." 
spt.SetMCFTime() 
print "Solving problem.." 
spt.SolveMCF() 

if spt.MCFGetStatus() == 0: 
  print "Optimal solution: %s" %spt.MCFGetFO() 
  print "Time elapsed: %s sec " %(spt.TimeMCF()) 
else: 
  print "Problem unfeasible!" 
  print "Time elapsed: %s sec " %(spt.TimeMCF()) 
```
