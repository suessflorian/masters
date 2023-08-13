import sqlite3
import matplotlib.pyplot as plt

# Set Matplotlib to use LaTeX and specify the default font family
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'

# Connect to the SQLite database
conn = sqlite3.connect('./data/files.db')
cursor = conn.cursor()

# Extract file sizes from the database
cursor.execute("SELECT size_in_bytes FROM files WHERE directory=\"./papers\"")
file_sizes = [row[0] for row in cursor.fetchall()]

# Bin the data
bin_counts, bin_edges, patches = plt.hist(
    file_sizes,
    bins=100,
    density=True)

# Alternate the colors of the bars
colors = ['black', 'grey']
for i, patch in enumerate(patches):
    patch.set_facecolor(colors[i % len(colors)])

plt.xscale('log')
plt.yscale('log')

# Removing the tick marks but keeping the labels
ax = plt.gca()
ax.tick_params(axis='both', which='both', length=0)

# Plotting
plt.title("Empirical PDF of File Size Distribution")
plt.xlabel("File Size (bytes)")
plt.ylabel("Probability Density")

# Save the figure
plt.savefig("./images/papers_size_pdf.png", dpi=300, bbox_inches='tight')

# Close the connection
conn.close()
