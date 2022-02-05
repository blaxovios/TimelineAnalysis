import pandas as pd
import matplotlib.pyplot as plt

output_file = r'C:\Users\tsepe\PycharmProjects\TimelineAnalysis\files\results.txt'

data = pd.read_csv(output_file,sep='\s+',header=None)[1:]
data = pd.DataFrame(data)

x = data[0]
y = data[1]
plt.plot(x, y,'b', label='Publications')
plt.grid()
plt.title('"Computer Graphics field publications per year"')
plt.xlabel('Year', fontsize = 15)
plt.ylabel('Publications', fontsize = 15)
plt.xticks(rotation=45)
plt.legend()
plt.show()