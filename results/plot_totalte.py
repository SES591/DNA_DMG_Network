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
    node_list=['ATM','p53','Mdm2','MdmX','Wip1','cyclinG','PTEN','p21','AKT','cyclinE','Rb','E2F1','p14ARF','Bcl2','Bax','caspase']

    t_total = np.zeros(18)
    normal_0 = read_te_from_file('te-all-step10-h%d-p53_0.dat'%(h))
    t_total[0] = sum(float(i) for i in normal_0)
    normal_1 = read_te_from_file('te-all-step10-h%d-p53_1.dat'%(h))
    t_total[1] = sum(float(i) for i in normal_1)

    count = 2
    for i in node_list:
        te = read_te_from_file('damaged/te-all-step10-h%d-p53_%s.dat'%(h,i))
        t_total[count] = sum(float(j) for j in te)
        count+=1

    x = ['p53_0','p53_1','ATM','p53','Mdm2','MdmX','Wip1','cyclinG','PTEN','p21','AKT','cyclinE','Rb','E2F1','p14ARF','Bcl2','Bax','caspase']
    x = np.array(x)
    idx = np.argsort(t_total)
    print t_total

    plt.figure(figsize=(15,10))
    plt.bar(range(18),t_total[idx])

    plt.xticks(range(18),x[idx],rotation='vertical')
    plt.ylabel('Total TE',weight='bold',size='large')
    plt.xlabel('Network Type',weight='bold',size='large')
    plt.title('Total TE of p53 networks for h=%d'%(h),weight='bold',size='large')
    plt.tight_layout(pad=2.5)
    plt.savefig("TE_total_single_node_h%d.png"%(h))
    plt.show()

if __name__=='__main__':
    main(sys.argv[1:])
