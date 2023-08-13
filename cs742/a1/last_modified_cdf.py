import sqlite3
import matplotlib.pyplot as plt
import numpy as np

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

# Plotting
plt.plot(file_sizes_sorted, y, marker='none', color='black', linestyle='-')

plt.xscale('log')
plt.yscale('log')

# Removing the tick marks but keeping the labels
ax = plt.gca()
ax.tick_params(axis='both', which='both', length=0)

plt.xlabel("Last Modified (epoch timestamp)")
plt.ylabel("CDF")
plt.title("CDF of File Size Distribution")

# Save the figure
plt.savefig("./images/last_modified_size_cdf.png", dpi=300, bbox_inches='tight')

# Close the connection
conn.close()
