import sys
import time_evol_ran as tev
import numpy as np

def main(argv):

   
    cmdargs = str(sys.argv)
    # Damage True or False
    damage = int(sys.argv[1])

    NODE_FILE = 'net-nodes-%d.dat'%(damage)
    
    for i in range(100):
        EDGE_FILE = 'results/random/local_%d/p53_%d-lr%03d.dat'%(damage,damage,i)
        tev.edge_print(EDGE_FILE,NODE_FILE,'p53_%d-lr%03d'%(damage,i),'local',damage)

        EDGE_FILE = 'results/random/global_%d/p53_%d-gr%03d.dat'%(damage,damage,i)
        tev.edge_print(EDGE_FILE,NODE_FILE,'p53_%d-gr%03d'%(damage,i),'global',damage)


if __name__=='__main__':
    main(sys.argv)
