import random
import sys
with open(sys.argv[1],'r') as source:
    data = [ (random.random(), line) for line in source ]
data.sort()
with open(sys.argv[1]+"_reshuffled",'w') as target:
    for _, line in data:
        target.write( line )
