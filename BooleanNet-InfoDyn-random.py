from BooleanNetInfoDyn import Bool_info
import sys

def main(argv):

    cmdargs = str(sys.argv)
    # Presence or absence of DNA damage
    damage = int(sys.argv[1])
    # Value for h
    h = int(sys.argv[2])
    # Type of random network; local or global.
    ran_type = str(sys.argv[3])


    if ran_type == 'local':
        ran_type_short = 'lr'
    elif ran_type == 'global':
        ran_type_short = 'gr'

    # Starting random network number
    Start_ran = int(sys.argv[4])
    # Ending random network number
    Stop_ran = int(sys.argv[5])
    
    NODE_FILE = 'net-nodes-%d.dat'%(damage)

    for i in range(Start_ran,Stop_ran+1):
        print 'Calculating TE for %s_%03d'%(ran_type_short,i)
        EDGE_FILE = 'results/random/%s_%d/p53_%d-%s%03d.dat'%(ran_type,damage,damage,ran_type_short,i)
        Bool_info(EDGE_FILE,NODE_FILE,10,h,'p53_%d-%s%03d'%(damage,ran_type_short,i))
    


if __name__=='__main__':
    main(sys.argv[1:])
