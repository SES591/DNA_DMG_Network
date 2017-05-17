import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

inhibit = [-2,-2,-3,-2,-3,-2,-2,-2,-2,-3,-4,-1,-1,-2,-3,-1,-3,-1,-3,-1,-2,-1,-1,-2,-1,-1,-1,-1]
activate = [1,2,1,1,2,1,1,2,1,2,2,2,3,1,2,1,1,1,2,2,3,1]

print len(inhibit), len(activate)

plt.title('Edge link weight counts for original network',weight='bold',size='x-large')
plt.ylabel('Count',weight='bold')
plt.xlabel('Weight',weight='bold')
plt.hist(inhibit,label='inhibit')
plt.hist(activate,label='activate')

plt.legend(loc='upper left')
plt.show()
