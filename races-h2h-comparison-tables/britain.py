import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Database path
db_path = '/Users/haatlason/Documents/GitHub/sqlite-greyjoy/capstone-ironislands/f1db.db'

# SQL query to retrieve the filtered race data for Race ID 1036, excluding specified columns
query = """
SELECT 
    race_id,
    type,
    position_display_order,
    position_number,
    driver_number,
    driver_id,
    constructor_id,
    engine_manufacturer_id,
    tyre_manufacturer_id,
    race_laps,
    race_time,
    race_gap,
    race_interval,
    race_points,
    race_qualification_position_number,
    race_grid_position_number,
    race_positions_gained,
    race_pit_stops,
    race_fastest_lap,
    race_driver_of_the_day,
    race_grand_slam
FROM 
    hamilton_verstappen_race_data_2021
WHERE 
    race_id = 1045 
    AND type = 'RACE_RESULT'
    AND (driver_id = 'lewis-hamilton' OR driver_id = 'max-verstappen');
"""

# Connect to the database and fetch data
conn = sqlite3.connect(db_path)
df = pd.read_sql_query(query, conn)
conn.close()

# Prepare the data for head-to-head table
hamilton_stats = df[df['driver_id'] == 'lewis-hamilton'].iloc[0]
verstappen_stats = df[df['driver_id'] == 'max-verstappen'].iloc[0]

# Construct a comparison table DataFrame
comparison_data = {
    "Stat": df.columns.drop(['race_id', 'driver_id']).tolist(),
    "Lewis Hamilton": [hamilton_stats[col] for col in df.columns if col not in ['race_id', 'driver_id']],
    "Max Verstappen": [verstappen_stats[col] for col in df.columns if col not in ['race_id', 'driver_id']]
}
comparison_df = pd.DataFrame(comparison_data)

# Display the table in a matplotlib plot
fig, ax = plt.subplots(figsize=(8, len(comparison_df) * 0.5))
ax.axis('tight')
ax.axis('off')

# Table data setup for matplotlib
table_data = [comparison_df.columns.tolist()] + comparison_df.values.tolist()
table = ax.table(cellText=table_data, cellLoc='center', loc='center')

# Formatting the table
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

header_color = '#3c3c3c'
cell_color_1 = '#87CEEB'  # Hamilton
cell_color_2 = '#FF0000'  # Verstappen

# Customize header
for j in range(3):
    cell = table[0, j]
    cell.set_fontsize(12)
    cell.set_text_props(weight='bold', color='white')
    cell.set_facecolor(header_color)

# Apply colors for each driver
for i in range(1, len(table_data)):
    table[i, 1].set_facecolor(cell_color_1)  # Lewis Hamilton column
    table[i, 2].set_facecolor(cell_color_2)  # Max Verstappen column

# Display the title and show plot
plt.title("Head-to-Head Comparison for Race Result in Great Britain GP", fontweight="bold", pad=20)
plt.show()
