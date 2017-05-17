import matplotlib.pyplot as plt
#import seaborn as sns
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


normal_all = read_te_from_file('te-all-step10-h1-p53_normal.dat')
normal_total = sum(float(i) for i in normal_all)    

gr_total = np.zeros(100)
lr_total = np.zeros(100)

for i in range(100):
    gr = read_te_from_file('random/global/te-all-step10-h1-p53-gr%03d.dat'%(i))
    lr = read_te_from_file('random/local/te-all-step10-h1-p53-lr%03d.dat'%(i))
    gr_total[i] = sum(float(j) for j in gr)
    lr_total[i] = sum(float(j) for j in lr)


data = [lr_total,gr_total,normal_total]
flierprops = dict(marker='o', markerfacecolor='black', markersize=2,
                  linestyle='none')
meanpointprops = dict(marker='D', markeredgecolor='black',
                      markerfacecolor='firebrick')
plt.boxplot(data,labels=['local','global','p53'],flierprops=flierprops,meanprops=meanpointprops,showmeans=True)

print np.mean(lr_total),min(lr_total),max(lr_total)
print np.mean(gr_total),min(gr_total),max(gr_total)

plt.ylabel('Total TE',weight='bold',size='large')
plt.xlabel('Network Type',weight='bold',size='large')
plt.title('Total TE of p53, local random, and global random networks.',weight='bold',size='large')
plt.tight_layout()
plt.savefig("TE_total.png")
plt.show()
