import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
from matplotlib.widgets import Button

def load_data(file_path):
    dataset = pd.read_csv(file_path)
    return dataset

def preprocess_data(dataset):
    dataset['PURPOSE'].fillna('NOT', inplace=True)
    dataset['START_DATE'] = pd.to_datetime(dataset['START_DATE'], errors='coerce')
    dataset['END_DATE'] = pd.to_datetime(dataset['END_DATE'], errors='coerce')
    
    dataset['date'] = dataset['START_DATE'].dt.date
    dataset['time'] = dataset['START_DATE'].dt.hour
    
    dataset['day-night'] = pd.cut(x=dataset['time'],
                                   bins=[0, 10, 15, 19, 24],
                                   labels=['Morning', 'Afternoon', 'Evening', 'Night'])
    
    dataset.dropna(inplace=True)
    dataset.drop_duplicates(inplace=True)
    return dataset

def plot_category_count(dataset):
    plt.figure()
    sns.countplot(data=dataset, x='CATEGORY')
    plt.xticks(rotation=90)
    plt.title('Category Count')
    plt.show()

def plot_purpose_count(dataset):
    plt.figure()
    sns.countplot(data=dataset, x='PURPOSE')
    plt.xticks(rotation=90)
    plt.title('Purpose Count')
    plt.show()

def plot_day_night_count(dataset):
    plt.figure()
    sns.countplot(x=dataset['day-night'])
    plt.title('Day-Night Distribution')
    plt.show()

def plot_purpose_vs_category(dataset):
    plt.figure()
    sns.countplot(data=dataset, x='PURPOSE', hue='CATEGORY')
    plt.title('Purpose vs Category')
    plt.xticks(rotation=90)
    plt.show()

def plot_monthly_data(dataset):
    dataset['MONTH'] = dataset['START_DATE'].dt.month
    month_label = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                   7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    dataset['MONTH'] = dataset['MONTH'].map(month_label)
    months = dataset['MONTH'].value_counts(sort=False)

    plt.figure()
    sns.lineplot(x=months.index, y=months.values)
    plt.title('Monthly Rides')
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.show()

def plot_weekday_data(dataset):
    dataset['DAY'] = dataset['START_DATE'].dt.weekday
    day_label = {0: 'Mon', 1: 'Tues', 2: 'Wed', 3: 'Thurs', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    dataset['DAY'] = dataset['DAY'].map(day_label)
    
    day_label_counts = dataset['DAY'].value_counts()

    plt.figure()
    sns.barplot(x=day_label_counts.index, y=day_label_counts.values)
    plt.xlabel('Day of the Week')
    plt.ylabel('Count')
    plt.title('Rides by Day of the Week')
    plt.show()

def on_click(event):
    plot_category_count(dataset)
    plot_purpose_count(dataset)
    plot_day_night_count(dataset)
    plot_purpose_vs_category(dataset)
    plot_monthly_data(dataset)
    plot_weekday_data(dataset)

def main():
    global dataset
    dataset = load_data("UberDataset.csv")
    dataset = preprocess_data(dataset)

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)

    ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
    btn = Button(ax_button, 'Plot Data')
    btn.on_clicked(on_click)

    plt.show()

main()
