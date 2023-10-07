import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')

bottom_2_5 = df['value'].quantile(0.025)
top_2_5 = df['value'].quantile(0.975)
# Clean data
df = df.query("value > @bottom_2_5 and value < @top_2_5")
df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")


def draw_line_plot():
  # Draw line plot
  fig, ax = plt.subplots(figsize=(32, 10), dpi=100)
  ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
  ax.set_xlabel("Date")
  ax.set_ylabel("Page Views")
  x_data = df['date'].values
  y_data = df['value'].values
  ax.plot(x_data, y_data, color='red')
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df_bar = df.copy()
  df_bar['Years'] = df_bar['date'].dt.strftime('%Y')
  df_bar['Months'] = df_bar['date'].dt.strftime('%B')
  df_bar = pd.DataFrame(
      df_bar.groupby(["Years", "Months"],
                     sort=False)["value"].mean().round().astype(int))
  df_bar = df_bar.rename(columns={"value": "Average Page Views"})
  df_bar = df_bar.reset_index()
  missing_data = {
      "Years": [2016, 2016, 2016, 2016],
      "Months": ['January', 'February', 'March', 'April'],
      "Average Page Views": [0, 0, 0, 0]
  }

  df_bar = pd.concat([pd.DataFrame(missing_data), df_bar])

  # Draw bar plot
  fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
  ax.set_title("Daily freeCodeCamp Forum Average Page Views per Month")

  sns.barplot(data=df_bar,
              x="Years",
              y="Average Page Views",
              hue="Months",
              palette="tab10")

  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig


def draw_box_plot():
  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box['Years'] = df_box['date'].dt.strftime('%Y')
  df_box['Months'] = df_box['date'].dt.strftime('%b')

  # Draw box plots (using Seaborn)
  fig, axes = plt.subplots(1, 2, figsize=(32, 10), dpi=100)
  sns.boxplot(x='Years', y='value', data=df_box, ax=axes[0])
  axes[0].set_title("Year-wise Box Plot (Trend)")
  axes[0].set_xlabel("Year")
  axes[0].set_ylabel("Page Views")
  month_order = [
      "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
      "Nov", "Dec"
  ]
  sns.boxplot(x='Months',
              y='value',
              data=df_box,
              order=month_order,
              ax=axes[1])
  axes[1].set_title("Month-wise Box Plot (Seasonality)")
  axes[1].set_xlabel("Month")
  axes[1].set_ylabel("Page Views")

  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
