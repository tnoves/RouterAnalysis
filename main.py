import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MultipleLocator

csv_path = "Eventlog_23-10-16-11.csv"


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
        if "DSL Link Up" in row:
            date = row[10:16]
            time = row[0:8]
            DSL_up.append((date, time))

current_year = datetime.now().year
dsl_down_timestamp = []
dsl_uptime_before_failure = []
dsl_back_up = []

for log in DSL_down:
    datetime_str = f"{log[0]} {current_year} {log[1]}"
    datetime_obj = datetime.strptime(datetime_str, "%d %b %Y %H:%M:%S")
    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    dsl_down_timestamp.append(formatted_datetime)
    dsl_uptime_before_failure.append(log[2])

for log in DSL_up:
    datetime_str = f"{log[0]} {current_year} {log[1]}"
    datetime_obj = datetime.strptime(datetime_str, "%d %b %Y %H:%M:%S")
    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    dsl_back_up.append(formatted_datetime)


print(dsl_down_timestamp)
print(dsl_uptime_before_failure)
print(dsl_back_up)

data_down = {'DSL Down': dsl_down_timestamp}
data_up = {'DSL Up': dsl_back_up}

df_set1 = pd.DataFrame(data_down)
df_set1['DSL Down'] = pd.to_datetime(df_set1['DSL Down'])
df_set1['Time'] = df_set1['DSL Down'].dt.hour

df_set2 = pd.DataFrame(data_up)
df_set2['DSL Up'] = pd.to_datetime(df_set2['DSL Up'])
df_set2['Time'] = df_set2['DSL Up'].dt.hour

# Create a full set of hours
all_hours = pd.DataFrame({'Time': range(24), 'Time': range(24)})

# Merge with actual data
df_set1 = all_hours.merge(df_set1, how='left', on='Time')
df_set2 = all_hours.merge(df_set2, how='left', on='Time')

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Create a heatmap for Set 1
heatmap_data_set1 = pd.pivot_table(df_set1, values='DSL Down', index='Time', aggfunc='count')
sns.heatmap(heatmap_data_set1.T, cmap='Reds', annot=True, fmt='g', cbar_kws={'label': 'Number of Downtimes'}, ax=ax1)

# Customize y-axis ticks and labels for Set 1
y_ticks_major_set1 = MultipleLocator(base=1)  # Major ticks every 1 hour
ax1.yaxis.set_major_locator(y_ticks_major_set1)

# Shift x-axis ticks by half an hour
ax1.set_xticks([tick for tick in range(24)])
# Customize x-axis labels to reflect the left edge of each bar
ax1.set_xticklabels([f"{int(tick)}:00" for tick in range(24)])

ax1.set_ylabel('Count of Downtimes')
ax1.set_title('Internet Downtime Hourly Aggregated Heatmap - Set 1')

# Create a heatmap for Set 2
heatmap_data_set2 = pd.pivot_table(df_set2, values='DSL Up', index='Time', aggfunc='count')
sns.heatmap(heatmap_data_set2.T, cmap='Greens', annot=True, fmt='g', cbar_kws={'label': 'Number of Ups'}, ax=ax2)

# Customize y-axis ticks and labels for Set 2
y_ticks_major_set2 = MultipleLocator(base=1)  # Major ticks every 1 hour
ax2.yaxis.set_major_locator(y_ticks_major_set2)

# Shift x-axis ticks by half an hour
ax2.set_xticks([tick for tick in range(24)])
# Customize x-axis labels to reflect the left edge of each bar
ax2.set_xticklabels([f"{int(tick)}:00" for tick in range(24)])

ax2.set_xlabel('Time')
ax2.set_ylabel('Count of Ups')
ax2.set_title('Internet Up Instances Hourly Aggregated Heatmap - Set 2')

plt.tight_layout()
plt.show()