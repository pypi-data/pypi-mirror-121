import numpy as np
import matplotlib.colors as colors

from colorsys import hls_to_rgb
from wordcloud import WordCloud


def create_word_cloud(entity_frequency_dict: dict,
                      parent_entity_dict: dict,
                      background_color: str = 'white',
                      width: int = 1000,
                      height: int = 1000,
                      max_words = 200):
    """

    Create the word cloud for the entities, with the size of the word
    been the frequency of the entity and the color of the word based on
    the cluster.

    :param entity_frequency_dict: dictionary with the relation entity-frequency
    :type entity_frequency_dict: ``dict``
    :param parent_entity_dict: dictionary with the relation parent-entities
    :type parent_entity_dict: ``dict``
    :param background_color: background color of the word cloud
    :type background_color: ``str``
    :param width: the width of the word cloud
    :type width: ``int``
    :param height: the height of the word cloud
    :type height: ``int``
    :return: the word cloud object
    """
    show_words_dict = dict(sorted(entity_frequency_dict.items(),
                                  key=lambda item: item[1],
                                  reverse=True)[:max_words])

    wc = WordCloud(background_color=background_color,
                   width=width,
                   height=height).generate_from_frequencies(
        show_words_dict)

    filtered_parent_entity_dict = filter_parents(show_words_dict,
                                                 parent_entity_dict)
    cluster_color_dict = create_dict_colors(filtered_parent_entity_dict)
    grouped_color_func = SimpleGroupedColorFunc(cluster_color_dict)
    wc.recolor(color_func=grouped_color_func)
    return wc


def filter_parents(dict_words, dict_parent):
    filtered_dict = {}
    for parent, entities in dict_parent.items():
        if any([entity in dict_words.keys() for entity in entities]):
            filtered_dict[parent] = entities
    return filtered_dict


def get_distinct_colors(n: int) -> list:
    """

    :param n: number of distinct colors.
    :type n: ``int``
    :return: list with the hex code of the colors.
    :rtype: ``list``
    """
    colors_list = []
    l = 0.55
    s = 0.7
    for h in np.arange(0., 1., 1. / n):
        hex_code = colors.to_hex(hls_to_rgb(h, l, s))
        colors_list.append(hex_code)

    return colors_list


def create_dict_colors(parent_entity_dict: dict) -> dict:
    """
    Change the key value of the parent-entity dictionary to the color code.

    :param parent_entity_dict: dictionary with the relation parent - entities.
    :type parent_entity_dict: ``dict``
    :return: dictionary with the relation color-entities.
    :rtype: ``dict``
    """
    max_cluster = len(parent_entity_dict)
    color_dict = {}
    k = 0
    list_color = get_distinct_colors(max_cluster)
    for value in parent_entity_dict.values():
        code_hex = list_color[k]
        k += 1
        color_dict[code_hex] = value
    return color_dict


def save_word_cloud(full_path, word_cloud):
    word_cloud.to_file(full_path)

class SimpleGroupedColorFunc(object):
    def __init__(self, color_to_words):
        """

        :param color_to_words:
        """
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

    def __call__(self, word, **kwargs):
        """

        :param word:
        :param kwargs:
        :return:
        """
        return self.word_to_color[word]
