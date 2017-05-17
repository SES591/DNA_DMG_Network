from BooleanNetInfoDyn import Bool_info
import sys

def main(argv):

    cmdargs = str(sys.argv)
    # Type of damage, edge or node
    damage_type = str(sys.argv[1])
    # Which damage list?
    damage_list = int(sys.argv[2])
    # Max Step Size
    maxStep = int(sys.argv[3])
    # history length
    historyLength = int(sys.argv[4])

    NODE_FILE = 'net-nodes-1.dat'
    EDGE_FILE = 'net-edges-1.dat'

    if damage_list == 0:
        node_list = ['ATM','p53','Mdm2','MdmX','Wip1','cyclinG','PTEN','p21']
        for i in node_list:
            print 'Calculating TE for %s damage.'%(i)
            Bool_info(EDGE_FILE,NODE_FILE,maxStep,historyLength,'p53_%s'%(i),damage_type,i)

    elif damage_list == 1:
        node_list = ['AKT','cyclinE','Rb','E2F1','p14ARF','Bcl2','Bax','caspase']
        for i in node_list:
            print 'Calculating TE for %s damage.'%(i)
            Bool_info(EDGE_FILE,NODE_FILE,maxStep,historyLength,'p53_%s'%(i),damage_type,i)


    elif damage_list == 2:
        edge_list = ['Wip1_ATM', 'cyclinG_ATM','E2F1_ATM','ATM_p53','Mdm2_p53','MdmX_p53','AKT_Mdm2', 'p14ARF_Mdm2','ATM_Mdm2','cyclinE_Mdm2']
        damage_node = 'none'

        for i in edge_list:
            EDGE_FILE = '%s.dat'%(i)
            print 'Calculating TE for %s damage.'%(i)
            Bool_info(EDGE_FILE,NODE_FILE,maxStep,historyLength,'p53_%s'%(i),damage_type,damage_node)

    elif damage_list == 3:
        edge_list = ['cyclinG_Mdm2','MdmX_Mdm2','p53_Mdm2','Rb_Mdm2','Wip1_Mdm2','ATM_MdmX','AKT_MdmX','p14ARF_MdmX','Mdm2_MdmX','Wip1_MdmX']
        damage_node = 'none'

        for i in edge_list:
            EDGE_FILE = '%s.dat'%(i)
            print 'Calculating TE for %s damage.'%(i)
            Bool_info(EDGE_FILE,NODE_FILE,maxStep,historyLength,'p53_%s'%(i),damage_type,damage_node)
   
    elif damage_list == 4:
        edge_list = ['p53_Wip1','p53_cyclinG','p53_PTEN','AKT_p21','Mdm2_p21', 'p53_p21','PTEN_AKT','E2F1_cyclinE','p21_cyclinE','ATM_Rb']
        damage_node = 'none'

        for i in edge_list:
            EDGE_FILE = '%s.dat'%(i)
            print 'Calculating TE for %s damage.'%(i)
            Bool_info(EDGE_FILE,NODE_FILE,maxStep,historyLength,'p53_%s'%(i),damage_type,damage_node)

    elif damage_list == 5:
        edge_list = ['cyclinE_Rb','caspase_Rb','Mdm2_Rb','p14ARF_E2F1','ATM_E2F1','Mdm2_E2F1','Rb_E2F1', 'E2F1_p14ARF','p53_p14ARF','Wip1_p14ARF']
        damage_node = 'none'

        for i in edge_list:
            EDGE_FILE = '%s.dat'%(i)
            print 'Calculating TE for %s damage.'%(i)
            Bool_info(EDGE_FILE,NODE_FILE,maxStep,historyLength,'p53_%s'%(i),damage_type,damage_node)

    elif damage_list == 6:
        edge_list = ['AKT_Bcl2','caspase_Bcl2','p53_Bcl2','Bcl2_Bax','p53_Bax','AKT_caspase','Bax_caspase', 'Bcl2_caspase','E2F1_caspase','p21_caspase']
        damage_node = 'none'

        for i in edge_list:
            EDGE_FILE = '%s.dat'%(i)
            print 'Calculating TE for %s damage.'%(i)
            Bool_info(EDGE_FILE,NODE_FILE,maxStep,historyLength,'p53_%s'%(i),damage_type,damage_node)
            
if __name__=='__main__':
    main(sys.argv[1:])
