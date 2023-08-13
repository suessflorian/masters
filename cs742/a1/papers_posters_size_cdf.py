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
cursor.execute("SELECT size_in_bytes FROM files WHERE directory=\"./papers\"")
paper_file_sizes = [row[0] for row in cursor.fetchall()]

# Create the CDF
papers_file_sizes_sorted = np.sort(paper_file_sizes)
papers_y = np.arange(1, len(papers_file_sizes_sorted) +
                     1) / len(papers_file_sizes_sorted)

# Extract file sizes from the database
cursor.execute("SELECT size_in_bytes FROM files WHERE directory=\"./posters\"")
poster_file_sizes = [row[0] for row in cursor.fetchall()]

# Create the CDF
poster_file_sizes_sorted = np.sort(poster_file_sizes)
posters_y = np.arange(1, len(poster_file_sizes_sorted) + 1) / \
    len(poster_file_sizes_sorted)

# Plotting
plt.plot(papers_file_sizes_sorted, papers_y,
         marker='none', color='black', linestyle='-', label="Papers")
plt.plot(poster_file_sizes_sorted, posters_y,
         marker='none', color='grey', linestyle='-', label="Posters")


plt.xscale('log')
plt.yscale('log')

# Removing the tick marks but keeping the labels
ax = plt.gca()
ax.tick_params(axis='both', which='both', length=0)

plt.xlabel("File Size (bytes)")
plt.ylabel("CDF")
plt.title("CDF of File Size Distribution")
plt.legend(loc='lower right')  # Added legend

# Save the figure
plt.savefig("./images/papers_posters_size_cdf.png",
            dpi=300, bbox_inches='tight')

plt.show()
# Close the connection
conn.close()
