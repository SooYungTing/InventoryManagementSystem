import pandas as pd
import matplotlib.pyplot as plt

# read the data from the Excel file
df = pd.read_excel('inventory.xlsx')

# create a line graph of item number versus quantity
plt.plot(df['Item_Number'], df['Quantity'], marker='o')

# add labels for each point
for i, row in df.iterrows():
    plt.annotate(row['Item_Number'], (row['Item_Number'], row['Quantity']))

# add labels and a title
plt.xlabel('Item Number')
plt.ylabel('Quantity')
plt.title('Item Number VS Quantity')

# show the graph
plt.show()


