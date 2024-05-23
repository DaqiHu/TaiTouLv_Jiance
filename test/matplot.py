import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mplcolors

# light to dark
red_colors = [mplcolors.to_rgb(hex_color) for hex_color in ["#fad6d9", "#e63946"]]
green_colors = [mplcolors.to_rgb(hex_color) for hex_color in ["#b5e3ce", "#1c4a35"]] # a better looking green color rather than default green (0, 1, 0)
blue_colors = [mplcolors.to_rgb(hex_color) for hex_color in ["#d8e6ee", "#457b9d"]] # a better looking blue color rather than default blue (0, 0, 1)


# Sample DataFrame
data = {
    'x': [1, 2, 3, 4, 5],
    'y': [1, 2, 3, 4, 5],
    'value': [0.1, 0.3, 0.5, 0.7, 0.9]
}
df = pd.DataFrame(data)

# Define color mappings
cmap = sns.color_palette([green_colors, blue_colors, red_colors])
norm = plt.Normalize(0, 1)

# Create the contour plot
sns.kdeplot(data=df, x='x', y='y', fill=True, cmap=cmap, levels=3, thresh=0, alpha=0.5, hue='value', hue_norm=norm)

# Add colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
plt.colorbar(sm)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Contour Plot with Custom Color Mapping')

plt.show()
