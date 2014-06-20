import matplotlib.pyplot as plt 
plt.rcParams['font.size'] = 11.
plt.rcParams['font.family'] = 'Comic Sans MS'
#plt.figure(facecolor="#336699")
ax = plt.subplot(111,axisbg='#D3DAE1')
plt.fill_between(recordsPerYear.keys(),recordsPerYear.values(),
         color='#333395',linewidth=1)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_color("#14293D")
ax.spines['left'].set_color("#14293D")
ax.tick_params(axis='x', colors='#14293D')
ax.tick_params(axis='y', colors='#14293D')
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
plt.xlim(1919,2011)
plt.xlabel("Year",color="#14293D")
plt.title("Number of Jazz Records Released",color="#14293D")
plt.xticks([1920,1930,1940,1950,1960,1970,1980,1990,2000,2010])
plt.show()