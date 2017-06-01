import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

def read_te_from_file(TE_FILE):
    te = []

    # Reads transfer entropy values from file
    for line in open(TE_FILE, 'r').readlines():
        items = [x.strip() for x in line.rstrip().split('\t')]
        #print items
        te = np.append(te,items[2])
    # Sorts the transfer entropy from largest to smallest before returning array.
    te = sorted(te,reverse=True)
    return te

def main(argv):
    cmdargs = str(sys.argv)
    h = int(sys.argv[1])

    edge_list = ['Wip1_ATM', 'cyclinG_ATM', 'E2F1_ATM', 'ATM_p53', 'Mdm2_p53', 'MdmX_p53', 'AKT_Mdm2',  'p14ARF_Mdm2', 'ATM_Mdm2', 'cyclinE_Mdm2', 'cyclinG_Mdm2', 'MdmX_Mdm2', 'p53_Mdm2', 'Rb_Mdm2', 'Wip1_Mdm2', 'ATM_MdmX', 'AKT_MdmX', 'p14ARF_MdmX', 'Mdm2_MdmX', 'Wip1_MdmX', 'p53_Wip1', 'p53_cyclinG', 'p53_PTEN', 'AKT_p21', 'Mdm2_p21', 'p53_p21', 'PTEN_AKT', 'E2F1_cyclinE', 'p21_cyclinE', 'ATM_Rb', 'cyclinE_Rb', 'caspase_Rb', 'Mdm2_Rb', 'p14ARF_E2F1', 'ATM_E2F1', 'Mdm2_E2F1', 'Rb_E2F1',  'E2F1_p14ARF', 'p53_p14ARF', 'Wip1_p14ARF', 'AKT_Bcl2', 'caspase_Bcl2', 'p53_Bcl2', 'Bcl2_Bax', 'p53_Bax', 'AKT_caspase', 'Bax_caspase', 'Bcl2_caspase', 'E2F1_caspase', 'p21_caspase']
    t_total = np.zeros(len(edge_list)+2)
    
    normal_0 = read_te_from_file('te-all-step10-h%d-p53_0.dat'%(h))
    t_total[0] = sum(float(i) for i in normal_0)
    normal_1 = read_te_from_file('te-all-step10-h%d-p53_1.dat'%(h))
    t_total[1] = sum(float(i) for i in normal_1)

    count = 2
    for edge in edge_list:
        te = read_te_from_file('damaged/te-all-step10-h%d-p53_%s.dat'%(h,edge))
        t_total[count] = sum(float(j) for j in te)
        count+=1

    x = ['p53_0','p53_1','Wip1_ATM', 'cyclinG_ATM', 'E2F1_ATM', 'ATM_p53', 'Mdm2_p53', 'MdmX_p53', 'AKT_Mdm2',  'p14ARF_Mdm2', 'ATM_Mdm2', 'cyclinE_Mdm2', 'cyclinG_Mdm2', 'MdmX_Mdm2', 'p53_Mdm2', 'Rb_Mdm2', 'Wip1_Mdm2', 'ATM_MdmX', 'AKT_MdmX', 'p14ARF_MdmX', 'Mdm2_MdmX', 'Wip1_MdmX', 'p53_Wip1', 'p53_cyclinG', 'p53_PTEN', 'AKT_p21', 'Mdm2_p21', 'p53_p21', 'PTEN_AKT', 'E2F1_cyclinE', 'p21_cyclinE', 'ATM_Rb', 'cyclinE_Rb', 'caspase_Rb', 'Mdm2_Rb', 'p14ARF_E2F1', 'ATM_E2F1', 'Mdm2_E2F1', 'Rb_E2F1',  'E2F1_p14ARF', 'p53_p14ARF', 'Wip1_p14ARF', 'AKT_Bcl2', 'caspase_Bcl2', 'p53_Bcl2', 'Bcl2_Bax', 'p53_Bax', 'AKT_caspase', 'Bax_caspase', 'Bcl2_caspase', 'E2F1_caspase', 'p21_caspase']
    x = np.array(x)
    idx = np.argsort(t_total)
    print t_total

    plt.figure(figsize=(15,10))
    plt.bar(range(len(x)),t_total[idx])

    plt.xticks(range(len(x)),x[idx],rotation='vertical')
    plt.xlim(xmin=0,xmax=len(x))
    plt.ylim(ymin=0,ymax=50)
    plt.ylabel('Total TE',weight='bold',size='large')
    plt.xlabel('Network Type',weight='bold',size='large')
    plt.title('Total TE of p53 networks for h=%d'%(h),weight='bold',size='large')
    plt.tight_layout(pad=2.5)
    plt.savefig("TE_total_single_edge_h%d.png"%(h))
    plt.show()
    
if __name__=='__main__':
    main(sys.argv[1:])
