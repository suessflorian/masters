import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Set Matplotlib to use LaTeX and specify the default font family
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'

# Connect to the SQLite database
conn = sqlite3.connect('./data/files.db')
cursor = conn.cursor()

# Extract file sizes from the database
cursor.execute("SELECT created_at FROM files")
file_sizes = [row[0] for row in cursor.fetchall()]

# Create the CDF
file_sizes_sorted = np.sort(file_sizes)
y = np.arange(1, len(file_sizes_sorted) + 1) / len(file_sizes_sorted)

# Convert UNIX timestamps to actual dates
dates = [datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d') for ts in file_sizes_sorted]

# Plotting
plt.plot(dates, y, marker='none', color='black', linestyle='-')

# Choose the start, end, and 3 evenly spaced dates in between
dates_to_display = [dates[0]]
indices_to_display = np.linspace(0, len(dates) - 1, 6)[1:-1].astype(int)  # excluding first and last
dates_to_display.extend([dates[i] for i in indices_to_display])
dates_to_display.append(dates[-1])

# Set the x-ticks to the chosen dates
plt.xticks(dates_to_display, rotation=45)

plt.xlabel("Last Modified Date")
plt.yscale('log')

# Removing the tick marks but keeping the labels
ax = plt.gca()
ax.tick_params(axis='both', which='both', length=0)

plt.ylabel("CDF")
plt.title("CDF of File Size Distribution")

# Save the figure
plt.tight_layout()  # Ensure the figure layout doesn't overlap
plt.savefig("./images/last_modified_size_cdf.png", dpi=300, bbox_inches='tight')

# Close the connection
conn.close()
