import pandas as pd

output_file = r'C:\Users\tsepe\PycharmProjects\TimelineAnalysis\files\results.txt'
data = pd.read_csv(output_file,sep='\s+',header=None)[1:]
data = pd.DataFrame(data)
data.columns =['Year', 'Publications']
data.to_clipboard()
data.to_csv(r'C:\Users\tsepe\PycharmProjects\TimelineAnalysis\files\results.csv', sep=';', index = False, header=True)