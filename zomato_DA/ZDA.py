import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Creating the data frame
dataframe = pd.read_csv("Zomato data .csv")
print(dataframe.head())

# Converting the datatype of "rate column to float" and removing the denominator
def handleRate(value):
    value = str(value).split('/')
    value = value[0]
    return float(value)

dataframe['rate'] = dataframe['rate'].apply(handleRate)
print(dataframe.head())
dataframe.info()

# Plot 1: Exploring the 'listed_in(type)' column
plt.figure()
sns.countplot(x=dataframe['listed_in(type)'])
plt.xlabel('Types of restaurant')
plt.title('Types of Restaurants and Votes')
plt.show()

time.sleep(1)  # Delay of 5 seconds before the next plot

# Plot 2: Plot showing votes for each type of restaurant
grouped_data = dataframe.groupby('listed_in(type)')['votes'].sum()
result = pd.DataFrame({'votes': grouped_data})

plt.figure()
plt.plot(result, c="green", marker="o")
plt.xlabel("Type of restaurant", c="red", size=20)
plt.ylabel("Votes", c="red", size=20)
plt.title('Votes by Type of Restaurant')
plt.show()

time.sleep(1)  # Delay of 5 seconds before the next plot

# Finding the restaurant name that received the max votes
max_votes = dataframe['votes'].max()
restaurant_with_max_votes = dataframe.loc[dataframe['votes'] == max_votes, 'name']
print("Restaurant(s) with the max votes:")
print(restaurant_with_max_votes)

# Plot 3: Approximate cost for two people
plt.figure()
couple_data = dataframe['approx_cost(for two people)']
sns.countplot(x=couple_data)
plt.title('Approximate Cost for Two People')
plt.show()

time.sleep(1)  # Delay of 5 seconds before the next plot

# Plot 4: Online or offline order comparison
plt.figure(figsize=(6,6))
sns.boxplot(x='online_order', y='rate', data=dataframe)
plt.title('Online vs Offline Orders Rating')
plt.show()

time.sleep(1)  # Delay of 5 seconds before the next plot

# Plot 5: Heatmap of restaurant types and online orders
pivot_table = dataframe.pivot_table(index='listed_in(type)', columns='online_order', aggfunc='size', fill_value=0)

plt.figure()
sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='d')
plt.title('Heatmap of Online Orders vs Restaurant Types')
plt.xlabel('Online Order')
plt.ylabel('Listed in (type)')
plt.show()
