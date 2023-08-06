import operator
import json

def create_parent_dict(entity_frequency_dict: dict,
                       entity_cluster_dict: dict) -> dict:
    """Create the dictionaries for entity - cluster name

    Receive one dictionary with the frequency of each entity (entity as key
    and frequency as value) and one dictionary with the cluster id (entity
    as key and cluster id as values). And create two dictionaries:

    * Entities_parent_dictionary: dictionary with the relation of entity
    and cluster name (parent). Entity as key and cluster name as value.

    * Parent_entities_dictionary: dictionary with the relation of cluster
    name(parent) and all entities in the cluster. Cluster name as key and
    list with all entities as value.

    :param entity_frequency_dict: dictionary entity as key and frequency as value.
    :type entity_frequency_dict: ``dict``
    :param entity_cluster_dict: dictionary entity as key and cluster id as value.
    :type entity_cluster_dict: ``dict``
    :return: dictionary with the relation parent - entities
    :rtype: ``dict``
    """
    parent_entity_dict = {}

    num_clusters = max(entity_cluster_dict.values()) + 1

    cluster_name = {}

    for entity, cluster in entity_cluster_dict.items():
        if parent_entity_dict.get(cluster, None):
            cluster_freq = entity_frequency_dict[cluster_name[cluster]]
            parent_entity_dict[cluster].append(entity)
            if entity_frequency_dict[entity] > cluster_freq:
                cluster_name.update({cluster: entity})
        else:
            parent_entity_dict[cluster] = [entity]
            cluster_name[cluster] = entity

    for k in range(num_clusters):
        parent_cluster = cluster_name[k]
        parent_entity_dict[parent_cluster] = parent_entity_dict.pop(k)

    return parent_entity_dict


def add_entities(relation_list: list,
                 parent_entity_dict: dict,
                 filtered_messages_dict: dict,
                 node_messages_examples: int) -> list:
    """Add entities to the relation list

    Create by adding the nodes and leaves of the three. The first value of
    the sub-list is the word to be printed, the second value is the id of
    the node (leaf), the third is the id of the parent node, and last the
    color.

    The first branch is the cluster name, the second is the entity and
    the last is the sample messages.


    :param relation_list: a list with the representation root of the tree.
    :type relation_list: ``list``
    :param parent_entity_dict: dictionary with the entity-cluster relation.
    :type parent_entity_dict: ``dict``
    :param filtered_messages_dict: dictioanry with the entity-message relation.
    :type filtered_messages_dict: ``dict``
    :param node_messages_examples: maximum of leaves in each branch.
    :type node_messages_examples: ``int``
    :return: a list with the representation of the tree.
    :rtype: ``list``
    """
    ind_cluster = len(parent_entity_dict)
    ind_entities = ind_cluster+1
    ind_message = ind_cluster + sum([len(value) for value in
                                     list(parent_entity_dict.values())]) + 1
    cluster_list = sorted_cluster(parent_entity_dict, filtered_messages_dict)
    for k in range(ind_cluster):
        cluster = cluster_list[k]
        relation_list += [[k+1, cluster[0], 0, 1, 'black']]
        for i in range(len(cluster[1])):
            value = cluster[1][i]
            freq_others = sum([freq for _, freq in
                                   cluster[2][i][node_messages_examples:]])
            freq_show = sum([freq for _, freq in
                                   cluster[2][i][:node_messages_examples]])
            relation_list += [[ind_entities, value, k + 1,
                               freq_others+freq_show, 'black']]
            if freq_others < 0.6*(freq_show+freq_others):
                for msg, freq in cluster[2][i][:node_messages_examples]:
                    relation_list += [[ind_message, msg, ind_entities,
                                        freq, 'black']]
                    ind_message += 1
                if len(cluster[2][i][node_messages_examples:]) > 0:
                    relation_list += [[ind_message, 'Outras frases', ind_entities,
                                        freq_others, 'black']]
                    ind_message += 1
            ind_entities += 1
    return relation_list


def sorted_cluster(parent_entity_dict: dict,
                   filtered_messages_dict: dict) -> list:
    """Sort cluster by frequency

    :param parent_entity_dict: dictionary with the relation entity-cluster.
    :type parent_entity_dict: ``dict``
    :param filtered_messages_dict: dictionary with the relation entity-message
    :type filtered_messages_dict: ``dict``
    :return: a list with the clusters, entities and message sorted by frequency
    :rtype: ``list``
    """
    output = []
    for key, value in parent_entity_dict.items():
        sorted_entity, freq, msg_list = sorted_entities(value,
                                                        filtered_messages_dict)
        aux_list = [key, sorted_entity, msg_list, freq]
        output.append(aux_list)
    return sorted(output, key=operator.itemgetter(3), reverse=True)


def sorted_entities(entities_list: list,
                    filtered_messages_dict: dict) -> tuple:
    """Sort entities by frequency

    :param entities_list: list with the entities of a cluster.
    :type entities_list: ``list``
    :param filtered_messages_dict: dictionary with the relation entity-message
    :type filtered_messages_dict: ``dict``
    :return: the sorted entities, the cumulative frequency and sorted messages.
    :rtype: ``tuple``
    """
    aux_list = []
    for entity in entities_list:
        sorted_messages = sorted(filtered_messages_dict[entity],
                                 key=operator.itemgetter(1), reverse=True)

        aux_list.append([entity, sorted_messages,
                         sum(value[1] for value in sorted_messages)])
    aux_list = sorted(aux_list, key=operator.itemgetter(2), reverse=True)
    entities_sorted = [value[0] for value in aux_list]
    msg_sorted = [value[1] for value in aux_list]
    freq = sum([value[2] for value in aux_list])
    return entities_sorted, freq, msg_sorted


def create_entity_hierarchy(filtered_messages_frequency_dict: dict,
                            parent_entity_dict: dict,
                            node_messages_examples: int) -> str:
    """Create the html with the tree representation

    :param filtered_messages_frequency_dict: dictionary with the relation entity-message
    :type filtered_messages_frequency_dict: ``dict``
    :param parent_entity_dict:  dictionary with the relation entity-cluster.
    :type parent_entity_dict: ``dict``
    :param node_messages_examples: maximum of leaves in a branch.
    :type node_messages_examples: ``int``
    :return: a string for the html
    :rtype: ``str``
    """
    relation_list = [[0, 'Agrupamento', -1, 1, 'black']]
    relation_list = add_entities(relation_list, parent_entity_dict,
                                 filtered_messages_frequency_dict,
                                 node_messages_examples)
    html = """<html>
      <head>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
          google.charts.load('current', {packages:['wordtree']});
          google.charts.setOnLoadCallback(drawSimpleNodeChart);
          function drawSimpleNodeChart() {
            var nodeListData = new google.visualization.arrayToDataTable([
              ['id', 'childLabel', 'parent', 'size', { role: 'style' }],
              %s);

            var options = {
              wordtree: {
                format: 'explicit',
                type: 'suffix'
              }
            };

            var wordtree = new google.visualization.WordTree(document.getElementById('wordtree_explicit'));
            wordtree.draw(nodeListData, options);
          }
        </script>
      </head>
      <body>
        <div id="wordtree_explicit" style="width: 1500px; height: 1200px;"></div>
      </body>
    </html>""" % (str(relation_list)[1:])
    return html


def create_parent_freq_dict(group_column: list) -> dict:
    """
    Create a dictionary with the name of the group and their frequency

    Example:
    {'cartão': 200, 'boleto': 100}

    :param group_column: A list with the groups of each sentence.
    :type group_column: `list`
    :return: A dictionary with the group name and their frequency
    :rtype: dict
    """
    parent_freq_dict = {}
    for row in group_column:
        row_unique = set(row)
        for entity in row_unique:
            parent_freq_dict[entity] = parent_freq_dict.get(entity, 0)+1
    return parent_freq_dict


def create_hierarchy_frequency_dict(entity_frequency_dict: dict,
                                      parent_entity_dict: dict,
                                      group_column: list) -> dict:
    """
    Create a dictionary as the example:

    {groups: [{name: cartão, frequency: 400, children: [{name: cartão de
    crédito, frequency: 129}, {name: cartão de débito, frequency: 81},
    name: cartão, frequency: 200}]}]}

    :param entity_frequency_dict: dictionary with the relation entity-frequency
    :type entity_frequency_dict: ``dict``
    :param parent_entity_dict: dictionary with the relation parent-entities
    :type parent_entity_dict: ``dict``
    :return: dictionary with information about the clusters.
    :rtype: ``dict``
    """
    parent_dict = create_parent_freq_dict(group_column)
    output_list = []
    for key, value in parent_entity_dict.items():
        hierarcy_frequency_dict = {'name': key,
                                   'frequency': parent_dict[key],
                                   'children': [{'name': entity,
                                                 'frequency': entity_frequency_dict[entity]}
                                                for entity in value]}
        output_list.append(hierarcy_frequency_dict)
    return {'group': output_list}

def save_entity_hierarchy(full_path, entity_hierarchy_html):
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(entity_hierarchy_html)

def save_entity_hierarchy_dict(full_path, entity_hierarchy_dict):
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(entity_hierarchy_dict, f, ensure_ascii=False)
