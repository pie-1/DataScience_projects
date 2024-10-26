import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from IPython.display import display, clear_output

# Loading the data
dataframe = pd.read_csv("Zomato data .csv")

# Converting the rate column
def handleRate(value):
    value = str(value).split('/')
    value = value[0]
    return float(value)

dataframe['rate'] = dataframe['rate'].apply(handleRate)

# Function to plot the graphs
def plot_graph(graph_index):
    plt.figure()

    if graph_index == 0:
        sns.countplot(x=dataframe['listed_in(type)'])
        plt.xlabel('Types of restaurant')
        plt.title('Types of Restaurants and Votes')

    elif graph_index == 1:
        grouped_data = dataframe.groupby('listed_in(type)')['votes'].sum()
        result = pd.DataFrame({'votes': grouped_data})
        plt.plot(result, c="green", marker="o")
        plt.xlabel("Type of restaurant", c="red", size=20)
        plt.ylabel("Votes", c="red", size=20)
        plt.title('Votes by Type of Restaurant')

    elif graph_index == 2:
        couple_data = dataframe['approx_cost(for two people)']
        sns.countplot(x=couple_data)
        plt.title('Approximate Cost for Two People')

    elif graph_index == 3:
        sns.boxplot(x='online_order', y='rate', data=dataframe)
        plt.title('Online vs Offline Orders Rating')

    elif graph_index == 4:
        pivot_table = dataframe.pivot_table(index='listed_in(type)', columns='online_order', aggfunc='size', fill_value=0)
        sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='d')
        plt.title('Heatmap of Online Orders vs Restaurant Types')
        plt.xlabel('Online Order')
        plt.ylabel('Listed in (type)')

    plt.show()

# Navigation function for buttons
def update_graph(change):
    global current_graph
    if change == 'forward':
        current_graph = (current_graph + 1) % 5
    elif change == 'backward':
        current_graph = (current_graph - 1) % 5
    
    clear_output(wait=True)
    plot_graph(current_graph)
    display(buttons)

# Initial graph index
current_graph = 0

# Creating forward and backward buttons
button_forward = widgets.Button(description="Forward")
button_backward = widgets.Button(description="Backward")

# Setting up button click actions
button_forward.on_click(lambda x: update_graph('forward'))
button_backward.on_click(lambda x: update_graph('backward'))

# Displaying the buttons
buttons = widgets.HBox([button_backward, button_forward])

# Display the first graph and buttons
plot_graph(current_graph)
display(buttons)
