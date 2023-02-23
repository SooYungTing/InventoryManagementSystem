import pandas as pd
import matplotlib.pyplot as plt

# read the data from the Excel file
df = pd.read_excel('inventory.xlsx')

# create a line graph
plt.plot(df.iloc[:, 0], df.iloc[:, 1])

# add labels and a title
plt.xlabel('Item Number')
plt.ylabel('Quantity')
plt.title('Item Number VS Quantity')

# show the graph
plt.show()

