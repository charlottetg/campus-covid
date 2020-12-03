import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

graph_stats = np.genfromtxt("/Users/annaspiro/Desktop/701/campus-covid/run1/graph_stats.csv", delimiter=',')
average_stats = np.genfromtxt("/Users/annaspiro/Desktop/701/campus-covid/run1/average_stats.csv", delimiter=',')
standard_devs = np.genfromtxt("/Users/annaspiro/Desktop/701/campus-covid/run1/standard_devs.csv", delimiter=',')
print(graph_stats)

# style
plt.style.use('seaborn-darkgrid')

x = range(8)
healthy = graph_stats[0]
asymptomatic = graph_stats[1]
quarantined = graph_stats[2]

plt.plot(x, healthy, label = "healthy")
plt.plot(x, asymptomatic, label = "asymptomatic")
plt.plot(x, quarantined, label = "quarantined")

# Add legend
plt.legend(bbox_to_anchor=(1, 1), loc="upper left")

plt.title("Population Sizes Throughout One Week of COVID Spread", loc='left', fontsize=12, fontweight=2, color='black')

plt.xlabel("Day After First COVID Infection")
plt.ylabel("Number of Students")

plt.tight_layout()

plt.show()
