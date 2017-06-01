import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

def plot_te(te,te_label,lw):
    
    x = [z for z in range(len(te))]
    #te_plot = plt.plot(x,te,'-o',label=te_label,marker = 'o',markersize=5,color=line_color)
    te_plot = plt.plot(x,te,'-',label=te_label,linewidth = lw)
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

    edge_list = ['Wip1_ATM', 'cyclinG_ATM', 'E2F1_ATM', 'ATM_p53', 'Mdm2_p53', 'MdmX_p53', 'AKT_Mdm2',  'p14ARF_Mdm2', 'ATM_Mdm2', 'cyclinE_Mdm2', 'cyclinG_Mdm2', 'MdmX_Mdm2', 'p53_Mdm2', 'Rb_Mdm2', 'Wip1_Mdm2', 'ATM_MdmX', 'AKT_MdmX', 'p14ARF_MdmX', 'Mdm2_MdmX', 'Wip1_MdmX', 'p53_Wip1', 'p53_cyclinG', 'p53_PTEN', 'AKT_p21', 'Mdm2_p21', 'p53_p21', 'PTEN_AKT', 'E2F1_cyclinE', 'p21_cyclinE', 'ATM_Rb', 'cyclinE_Rb', 'caspase_Rb', 'Mdm2_Rb', 'p14ARF_E2F1', 'ATM_E2F1', 'Mdm2_E2F1', 'Rb_E2F1',  'E2F1_p14ARF', 'p53_p14ARF', 'Wip1_p14ARF', 'AKT_Bcl2', 'caspase_Bcl2', 'p53_Bcl2', 'Bcl2_Bax', 'p53_Bax', 'AKT_caspase', 'Bax_caspase', 'Bcl2_caspase', 'E2F1_caspase', 'p21_caspase']
    
    plt.figure(figsize=(15,10))
    normal_0 = read_te_from_file('te-all-step10-h%d-p53_0.dat'%(h))
    normal_1 = read_te_from_file('te-all-step10-h%d-p53_1.dat'%(h))
    plot_te(normal_0,'p53 No Dmg',3.0)
    plot_te(normal_1,'p53 Dmg',3.0)
    
    for edge in edge_list:
        edge_te = edge
        edge_te = read_te_from_file('damaged/te-all-step10-h%d-p53_%s.dat'%(h,edge))
        plot_te(edge_te,'%s'%(edge),1.0)

    plt.legend(loc='upper right',fontsize='small',ncol=3)
    plt.tick_params(axis='both',which='major', labelsize='large')
    #sns.axes_style("darkgrid", {"axes.facecolor": ".9"})
    #plt.yscale('log')
    #plt.xscale('log')
    plt.xlabel('Rank',size='x-large',weight='bold')
    plt.ylabel('Transfer Entropy',size='x-large',weight='bold')
    plt.title('Transfer Entropy for p53 network and single edge knockout, h=%d'%(h),size='xx-large',weight='bold')
    plt.xlim(xmin=0.0,xmax=255)
    plt.ylim(ymin=0.0,ymax=1.0)
    plt.margins(0.2)
    plt.tight_layout(pad=2.5)
    plt.savefig("TE_single_edge_h%d.png"%(h))
    plt.show()
    
if __name__=='__main__':
    main(sys.argv[1:])
