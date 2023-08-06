import numpy as np

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_distances


class EntityCluster:
    """Wraps methods for entities clustering.

    Attributes
    ----------
    sim_threshold : float
        Clustering similarity threshold.

    Methods
    -------
    cluster_entities(entities_embedding)
        Clusters a group of entities.

    # TODO: add public methods
    """

    def __init__(self, sim_threshold: float = 0.65):
        """
        Parameters
        ----------
        sim_threshold : float, optional
            Similarity threshold;
        """
        self.sim_threshold = sim_threshold

    def cluster_entities(self, entities_embedding: dict) -> dict:
        """Clusters a group of entities.

        Parameters
        ----------
        entities_embedding : dict
            Entities and their embedding representation.

        Returns
        -------
        dict
            Entity (key) to cluster number (value) mapping.
        """
        entity_cluster_dict = {}
        entities_array = np.array(list(entities_embedding.values()))
        thr = self.__calculate_threshold(entities_array)
        agglomerative = AgglomerativeClustering(n_clusters=None,
                                                linkage='complete',
                                                affinity='cosine',
                                                distance_threshold=thr
                                                ).fit(entities_array)

        keys = list(entities_embedding.keys())
        for k in range(len(keys)):
            key = keys[k]
            entity_cluster_dict[key] = agglomerative.labels_[k]
        return entity_cluster_dict

    def __calculate_threshold(self, entities_embeddig: np.array) -> float:
        """Calculates distance threshold.

        Calculates the distance threshold over the similarity matrix of a
        dataset, using a minimum value of similarity between the clusters.

        Parameters
        ----------
        entities_embeddig : np.array
            Entities and their embedding representation.

        Returns
        -------
        float
            Threshold of distance for a level of similarity.
        """
        cos = cosine_distances(entities_embeddig)
        return (1 - self.sim_threshold) * cos.max()
