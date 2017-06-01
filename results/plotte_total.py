import matplotlib.pyplot as plt
#import seaborn as sns
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

def total_te(te):
    total = sum(float(i) for i in te)
    return total

def main(argv):
    cmdargs = str(sys.argv)
    h = int(sys.argv[1])
     
    normal_0 = read_te_from_file('te-all-step10-h%d-p53_0.dat'%(h))
    normal_0_total = total_te(normal_0)
    normal_1 = read_te_from_file('te-all-step10-h%d-p53_1.dat'%(h))
    normal_1_total = total_te(normal_1)

    gr_0_total = np.zeros(100)
    gr_1_total = np.zeros(100)
    lr_0_total = np.zeros(100)
    lr_1_total = np.zeros(100)

    edge_list = ['Wip1_ATM', 'cyclinG_ATM', 'E2F1_ATM', 'ATM_p53', 'Mdm2_p53', 'MdmX_p53', 'AKT_Mdm2',  'p14ARF_Mdm2', 'ATM_Mdm2', 'cyclinE_Mdm2', 'cyclinG_Mdm2', 'MdmX_Mdm2', 'p53_Mdm2', 'Rb_Mdm2', 'Wip1_Mdm2', 'ATM_MdmX', 'AKT_MdmX', 'p14ARF_MdmX', 'Mdm2_MdmX', 'Wip1_MdmX', 'p53_Wip1', 'p53_cyclinG', 'p53_PTEN', 'AKT_p21', 'Mdm2_p21', 'p53_p21', 'PTEN_AKT', 'E2F1_cyclinE', 'p21_cyclinE', 'ATM_Rb', 'cyclinE_Rb', 'caspase_Rb', 'Mdm2_Rb', 'p14ARF_E2F1', 'ATM_E2F1', 'Mdm2_E2F1', 'Rb_E2F1',  'E2F1_p14ARF', 'p53_p14ARF', 'Wip1_p14ARF', 'AKT_Bcl2', 'caspase_Bcl2', 'p53_Bcl2', 'Bcl2_Bax', 'p53_Bax', 'AKT_caspase', 'Bax_caspase', 'Bcl2_caspase', 'E2F1_caspase', 'p21_caspase']
    
    node_list=['ATM','p53','Mdm2','MdmX','Wip1','cyclinG','PTEN','p21','AKT','cyclinE','Rb','E2F1','p14ARF','Bcl2','Bax','caspase']

    edge_total = np.zeros(len(edge_list))
    node_total = np.zeros(len(node_list))
    
    count = 0
    for edge in edge_list:
        edge_te = read_te_from_file('damaged/te-all-step10-h%d-p53_%s.dat'%(h,edge))
        edge_total[count] = total_te(edge_te)
        count += 1
    
    count = 0
    for node in node_list:
        node_te = read_te_from_file('damaged/te-all-step10-h%d-p53_%s.dat'%(h,node))
        node_total[count] = total_te(node_te)
        count += 1
        
    for i in range(100):
        gr_0 = read_te_from_file('random/global_0/te-all-step10-h%d-p53_0-gr%03d.dat'%(h,i))
        gr_1 = read_te_from_file('random/global_1/te-all-step10-h%d-p53_1-gr%03d.dat'%(h,i))
        lr_0 = read_te_from_file('random/local_0/te-all-step10-h%d-p53_0-lr%03d.dat'%(h,i))
        lr_1 = read_te_from_file('random/local_1/te-all-step10-h%d-p53_1-lr%03d.dat'%(h,i))
        gr_0_total[i] = total_te(gr_0)
        gr_1_total[i] = total_te(gr_1)
        lr_0_total[i] = total_te(lr_0)
        lr_1_total[i] = total_te(lr_1)

    data = [lr_0_total,lr_1_total,gr_0_total,gr_1_total,normal_0_total,normal_1_total,edge_total,node_total]
    flierprops = dict(marker='o', markerfacecolor='black', markersize=2,
                  linestyle='none')
    meanpointprops = dict(marker='D', markeredgecolor='black',
                      markerfacecolor='firebrick')
                      
    plt.figure(figsize=(15,10))            
    plt.boxplot(data,labels=['local_0', 'local_1', 'global_0', 'global_1', 'p53_0', 'p53_1', 'edge_knockout', 'node_knockout'], flierprops=flierprops, meanprops=meanpointprops, showmeans=True)

    #print np.mean(gr_0_total),min(gr_0_total),max(gr_0_total)
    #print np.mean(gr_1_total),min(gr_1_total),max(gr_1_total)
    #print np.mean(lr_0_total),min(lr_0_total),max(lr_0_total)
    #print np.mean(lr_1_total),min(lr_1_total),max(lr_1_total)
    plt.ylim(ymin=0,ymax=50)
    plt.ylabel('Total TE',weight='bold',size='large')
    plt.xlabel('Network Type',weight='bold',size='large')
    plt.title('Total TE of networks for h=%d.'%(h), weight='bold', size='x-large')
    plt.tight_layout(pad=2.5)
    plt.savefig("TE_total_h%d.png"%(h))
    plt.show()

if __name__=='__main__':
    main(sys.argv[1:])
