import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def plot_topic_distribution(song_mapping: dict, out_path: Path) -> None:
    """Plot and save a bar chart showing the number of songs per topic."""
    df = pd.DataFrame(list(song_mapping.items()), columns=["Song", "Topic"])
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x="Topic", ax=ax, palette="viridis", hue="Topic", legend=False)
    ax.set_title("Number of Songs per Topic")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)