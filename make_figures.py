import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

graph_stats = np.genfromtxt("/Users/annaspiro/Desktop/701/campus-covid/run3/graph_stats.csv", delimiter=',')
average_stats = np.genfromtxt("/Users/annaspiro/Desktop/701/campus-covid/run3/average_stats.csv", delimiter=',')
standard_devs = np.genfromtxt("/Users/annaspiro/Desktop/701/campus-covid/run3/standard_devs.csv", delimiter=',')
print(graph_stats)

# style
plt.style.use('seaborn-darkgrid')

x = range(8)
#healthy = graph_stats[0]
av_asymptomatic = average_stats[1]
av_quarantined = average_stats[2]

asymptomatic_error = standard_devs[1]
quarantined_error = standard_devs[2]

#plt.plot(x, healthy, label = "healthy")
plt.plot(x, av_asymptomatic, label = "asymptomatic", color = "red")
plt.plot(x, av_quarantined, label = "quarantined", color = "blue")

plt.fill_between(x, av_quarantined+quarantined_error, av_quarantined-quarantined_error, alpha=0.2)
plt.fill_between(x, av_asymptomatic+asymptomatic_error, av_asymptomatic-asymptomatic_error, alpha=0.2)

# Add legend
plt.legend(bbox_to_anchor=(1, 1), loc="upper left")

plt.title("Asymptomatic and Quarantined Populations (Averaged)", loc='left', fontsize=12, fontweight=2, color='black')

plt.xlabel("Days After First COVID-19 Infection")
plt.ylabel("Number of Students")

plt.tight_layout()

plt.show()
