import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

def plot_te(te,te_label,line_color,lw):
    
    x = [z for z in range(len(te))]
    #te_plot = plt.plot(x,te,'-o',label=te_label,marker = 'o',markersize=5,color=line_color)
    te_plot = plt.plot(x,te,'-',label=te_label,color=line_color,linewidth = lw)
    return te_plot

def plot_te_error(te,err_min,err_max,te_label,line_color,lw):
    x = [z for z in range(len(te))]
    #te_plot = plt.plot(x,te,'-o',label=te_label,marker = 'o',markersize=5,color=line_color)
    te_plot = plt.errorbar(x, te, yerr=[err_min,err_max],label=te_label,fmt='-o',capthick=1)
    return te_plot

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
    normal_nodmg = read_te_from_file('te-all-step10-h%d-p53_0.dat'%(h))
    normal_dmg = read_te_from_file('te-all-step10-h%d-p53_1.dat'%(h))
    
    plt.figure(figsize=(15,10))

    plot_te(normal_nodmg,'No Damage','blue',2.0)
    plot_te(normal_dmg,'Damage','red',2.0)

    g = np.zeros((100,len(normal_nodmg)))
    l = np.zeros((100,len(normal_nodmg)))

    for i in range(100):
        gr_name = 'gr%03d'%(i)
        lr_name = 'lr%03d'%(i)
        gr = read_te_from_file('random/global_0/te-all-step10-h%d-p53_0-gr%03d.dat'%(h,i))
        lr = read_te_from_file('random/local_0/te-all-step10-h%d-p53_0-lr%03d.dat'%(h,i))
        for j in range(len(gr)):
            g[i,j] = gr[j]
            l[i,j] = lr[j]
        
    g_mean = np.zeros(len(gr))
    l_mean = np.zeros(len(lr))
    l_min = np.zeros(len(lr))
    l_max = np.zeros(len(lr))
    g_min = np.zeros(len(gr))
    g_max = np.zeros(len(gr))

    for i in range(len(gr)):
        g_mean[i] = g[:,i].mean(axis=0)
        l_mean[i] = l[:,i].mean(axis=0)
        l_min[i] = np.amin(l[:,i])
        l_max[i] = np.amax(l[:,i])
        g_min[i] = np.amin(g[:,i])
        g_max[i] = np.amax(g[:,i])

    plot_te_error(l_mean,abs(l_min-l_mean),abs(l_max-l_mean),'local','green',2.0)
    plot_te_error(g_mean,abs(g_min-g_mean),abs(g_max-g_mean),'global','green',2.0)

    plt.legend(loc='upper right',fontsize='large')
    plt.tick_params(axis='both',which='major', labelsize='large')
    #sns.axes_style("darkgrid", {"axes.facecolor": ".9"})
    #plt.yscale('log')
    #plt.xscale('log')
    plt.xlabel('Rank',size='x-large',weight='bold')
    plt.ylabel('Transfer Entropy',size='x-large',weight='bold')
    plt.title('Transfer Entropy for p53 network and random networks, h=%d'%(h),size='xx-large',weight='bold')
    plt.xlim(xmin=0.0,xmax=255)
    plt.ylim(ymin=0.0,ymax=1.0)
    plt.margins(0.2)
    plt.tight_layout(pad=2.5)
    plt.savefig("TE_h%d.png"%(h))
    plt.show()
    
if __name__=='__main__':
    main(sys.argv[1:])
