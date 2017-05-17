import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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


node_list=['ATM','p53','Mdm2','MdmX','Wip1','cyclinG','PTEN','p21','AKT','cyclinE','Rb','E2F1','p14ARF','Bcl2','Bax','caspase']

t_total = np.zeros(18)
normal_0 = read_te_from_file('te-all-step10-h5-p53_0.dat')
t_total[0] = sum(float(i) for i in normal_0)
normal_1 = read_te_from_file('te-all-step10-h5-p53_1.dat')
t_total[1] = sum(float(i) for i in normal_1)

count = 2
for i in node_list:
    te = read_te_from_file('damaged/te-all-step10-h5-p53_%s.dat'%(i))
    t_total[count] = sum(float(j) for j in te)
    count+=1

x = ['p53_0','p53_1','ATM','p53','Mdm2','MdmX','Wip1','cyclinG','PTEN','p21','AKT','cyclinE','Rb','E2F1','p14ARF','Bcl2','Bax','caspase']
idx =np.argsort(t_total)
print t_total


plt.bar(range(18),t_total)

plt.xticks(range(18),x,rotation='vertical')
plt.ylabel('Total TE',weight='bold',size='large')
plt.xlabel('Network Type',weight='bold',size='large')
plt.title('Total TE of p53 networks for h=5',weight='bold',size='large')
plt.tight_layout()
plt.savefig("TE_total_single_node_h5.png")
plt.show()
