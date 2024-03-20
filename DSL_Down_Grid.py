import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

csv_path = "eventlog_complete.csv"


DSL_down = []
DSL_up = []

with open(csv_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_file:
        if "DSL Link Down" in row:
            date = row[10:16]
            time = row[0:8]
            uptime = row[46:].rstrip(" seconds\n")
            DSL_down.append((date, time, uptime))

current_year = datetime.now().year
dsl_down_timestamp = []
dsl_uptime_before_failure = []

for log in DSL_down:
    datetime_str = f"{log[0]} {current_year} {log[1]}"
    datetime_obj = datetime.strptime(datetime_str, "%d %b %Y %H:%M:%S")
    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    dsl_down_timestamp.append(formatted_datetime)
    dsl_uptime_before_failure.append(log[2])

print(dsl_down_timestamp)
print(dsl_uptime_before_failure)
print(len(dsl_down_timestamp))

data_down = {'DSL Down': dsl_down_timestamp}

df_set1 = pd.DataFrame(data_down)
df_set1['DSL Down'] = pd.to_datetime(df_set1['DSL Down'])

# Extract day and hour from the timestamp
df_set1['Day'] = df_set1['DSL Down'].dt.date
df_set1['Time'] = df_set1['DSL Down'].dt.hour

# Create a complete set of hours and days
all_days = pd.date_range(df_set1['Day'].min(), df_set1['Day'].max(), freq='D')
all_hours = range(24)
all_combinations = [(day, hour) for day in all_days for hour in all_hours]
full_index = pd.MultiIndex.from_tuples(all_combinations, names=['Day', 'Time'])
full_df = pd.DataFrame(index=full_index).reset_index()

# Convert 'Day' column to datetime to match types
full_df['Day'] = pd.to_datetime(full_df['Day'])

# Concatenate the actual data with the complete set and fill NaN values with 0
df_set1 = pd.concat([full_df, df_set1], axis=0, ignore_index=True).fillna(0)

# Ensure 'Day' is datetime type for comparison in the pivot table
df_set1['Day'] = pd.to_datetime(df_set1['Day'])

# Aggregate the data to handle potential duplicates
df_set1_agg = df_set1.groupby(['Day', 'Time']).size().reset_index(name='Counts')

# Create subplots
fig, (ax1) = plt.subplots(1, 1, figsize=(12, 10), sharex=True)

# Create a pivot table for Set 1 and subtract 1 from every cell (this corrects the count from creating a complete table)
heatmap_data_set1 = df_set1_agg.pivot(index='Day', columns='Time', values='Counts').fillna(0) - 1
sns.heatmap(heatmap_data_set1, cmap='Reds', annot=True, fmt='g', cbar_kws={'label': 'Number of Downtimes'},
            linewidths=0.5, linecolor='black', ax=ax1)

# Customize y-axis ticks and labels for Set 1
ax1.set_yticks([tick + 0.5 for tick in range(len(heatmap_data_set1))])
ax1.set_yticklabels([str(date.date()) for date in heatmap_data_set1.index])

# Customize x-axis ticks and labels
ax1.set_xticks(range(24))
ax1.set_xticklabels([f"{hour:02d}:00" for hour in range(24)])

ax1.set_ylabel('Date')
ax1.set_xlabel('Hour')
ax1.set_title('Internet Downtime Hourly Heatmap')

plt.tight_layout()
plt.show()