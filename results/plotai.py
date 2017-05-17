import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_ai(ai,ai_label,line_color,lw):
    
    x = [z for z in range(len(ai))]
    ai_plot = plt.plot(x,ai,'-',label=ai_label,color=line_color,linewidth = lw)
    return ai_plot

def read_ai_from_file(AI_FILE):
    ai = []

    # Reads transfer entropy values from file
    for line in open(AI_FILE, 'r').readlines():
        items = [x.strip() for x in line.rstrip().split('\t')]
        #print items
        ai = np.append(ai,items[1])
    # Sorts the transfer entropy from largest to smallest before returning array.
    ai = sorted(ai,reverse=True)
    return ai


normal_all = read_ai_from_file('ai-all-step10-h1-p53_normal.dat')

plt.figure(figsize=(15,10))
plot_ai(normal_all,'p53 Normal','black',2.0)

gr_total = np.zeros(len(normal_all))
lr_total = np.zeros(len(normal_all))

for i in range(100):
    gr_name = 'gr%03d'%(i)
    lr_name = 'lr%03d'%(i)
    gr = read_ai_from_file('random/global/ai-all-step10-h1-p53-gr%03d.dat'%(i))
    lr = read_ai_from_file('random/local/ai-all-step10-h1-p53-lr%03d.dat'%(i))
    for j in range(len(gr)):
        gr_total[j] = gr_total[j] + float(gr[j])
        lr_total[j] = lr_total[j] + float(lr[j])
    plot_ai(gr,gr_name,'blue',0.5)
    plot_ai(lr,lr_name,'green',0.5)

plot_ai(gr_total/100.0,'Global Random Mean','blue',2.0)
plot_ai(lr_total/100.0,'Local Random Mean','green',2.0)

#plt.legend(loc='upper right',fontsize='large')
plt.tick_params(axis='both',which='major', labelsize='large')
sns.axes_style("darkgrid", {"axes.facecolor": ".9"})
#plt.yscale('log')
#plt.xscale('log')
plt.xlabel('Rank',size='x-large',weight='bold')
plt.ylabel('Active Information',size='x-large',weight='bold')
plt.title('Active Information for p53 network and random networks',size='xx-large',weight='bold')
plt.xlim(xmin=0.0)
plt.xticks(np.arange(0, 17, 1.0))
plt.ylim(ymin=0.0,ymax=1.0)
plt.margins(0.2)
plt.tight_layout(pad=2.5)
#plt.savefig("AI_average_all.png")
#plt.savefig("TE_local.pdf")
plt.show()
