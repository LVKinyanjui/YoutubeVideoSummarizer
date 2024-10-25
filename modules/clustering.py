# %%
from umap import UMAP
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from .embeddings import get_embeddings  # The . mitigates possible import error

# %%
def visualize(vis_dims: np.array, kmeans_clusters: list):
    x = [x for x, y in vis_dims]
    y = [y for x, y in vis_dims]
    
    num_clusters = len(set(kmeans_clusters))  # Number of unique clusters
    cmap = plt.cm.get_cmap("viridis", num_clusters)  # Generate a colormap with `num_clusters` colors

    fig, ax = plt.subplots()  # Create a figure and axis for further processing

    for category in range(num_clusters):
        color = cmap(category)  # Get a distinct color for each cluster
        xs = np.array(x)[kmeans_clusters == category]
        ys = np.array(y)[kmeans_clusters == category]
        ax.scatter(xs, ys, color=color, alpha=0.3)

        # Calculate the cluster center
        avg_x = xs.mean()
        avg_y = ys.mean()

        # Plot the center point with a marker
        ax.scatter(avg_x, avg_y, marker="x", color=color, s=100)

    return fig  # Return the figure instance for further processing

# %%
def show_text_clusters(texts: list[str], n_clusters=5):

    # TODO: Implement a 2048 token limit on input text(s)

    embeddings = get_embeddings(texts)
    if isinstance(texts, list):
        if len(embeddings) != len(texts):
            raise ValueError("Returned embedding list not equal to input text list to the embedding model")
    # df["embeddings"] = embeddings
    # df.head(2)

    kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42)
    kmeans.fit(embeddings)
    # df['Cluster'] = kmeans.labels_

    reducer = UMAP(random_state=42)
    latent_embedding = reducer.fit_transform(embeddings)

    fig = visualize(latent_embedding, kmeans.labels_)
    return fig

# %%
if __name__ == '__main__':
    df = pd.read_table("../data/comments.csv",header=None, names=["comments"])
    show_text_clusters(df.comments.to_list())

# %%



