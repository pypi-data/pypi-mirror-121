class Embedding:
    """Wraps methods for embedding creation and convertion.

    Attributes
    ----------
    embedding
        Word embedding.

    Methods
    -------
    create_entities_embeddings(entity_postagging_dict)
        Return a dictionary with the representation of the entities.
    """

    def __init__(self, embedding) -> None:
        """
        Parameters
        ----------
        embedding
            Word embedding.
        """
        self.embedding = embedding

    def create_entities_embeddings(self, entity_postagging_dict: dict) -> dict:
        """Return a dictionary with the representation of the entities.

        Parameters
        ----------
        entity_postagging_dict : dict
            Dictionary with the entity as key and POSTagging of the 
            entity as value.

        Returns
        -------
        dict
            Dictionary with the entity as key and the embedding 
            representation of the entity as value.
        """

        entities_embeddings_dict = {}
        for word in entity_postagging_dict.keys():
            if len(word.split()) > 1:
                tags = entity_postagging_dict[word]
                entities_embeddings_dict[word] = self.__convert_sent2vec(word,
                                                                         tags)
            else:
                entities_embeddings_dict[word] = self.__convert_word2vec(word)
        return entities_embeddings_dict

    def __convert_word2vec(self, word: str) -> list:
        """Get the embedding representation of a single word.

        Parameters
        ----------
        word : str
            Entity to get the embedding representation.

        Returns
        -------
        list
            Embedding representation.
        """
        return self.embedding[word].tolist()

    def __convert_sent2vec(self, words: str, postag: str) -> list:
        """Get the embedding representation of a compound word.

        Calculates a numerical representation of each word 
        inside words, which will be the average of them. 
        The method ignores prepositions or conjunctions.

        Parameters
        ----------
        words : str
            Entities to get the embedding representation.
        postag : str
            Description

        Returns
        -------
        list
            Embedding representation.
        """
        representation = []
        words_lst = words.split()
        postag_lst = postag.split()
        length = len(words_lst)
        for k in range(len(words_lst)):
            if postag_lst[k] in ['PREP', 'CONJ']:
                length = length - 1
            else:
                representation.append(self.embedding[words_lst[k]])
        value = sum(representation)
        value = value / length
        return value.tolist()
