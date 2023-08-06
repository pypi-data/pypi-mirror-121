from math import floor


def filter_entity(entities_column, entities_to_keep, field_name):
    filtered_entities_list = []
    for entities_list in entities_column:
        if len(entities_list) > 0:
            filtered_list = [entity_dict for entity_dict in entities_list
                             if entity_dict[field_name] in entities_to_keep]
        else:
            filtered_list = []
        filtered_entities_list.append(filtered_list)
    return filtered_entities_list


def filter_entity_type(entities_column):
    entity_list = filter_entity(
        entities_column=entities_column,
        entities_to_keep={'generic_entity', 'financial'},
        field_name='type')
    return entity_list


def filter_entity_frequency(entities_column, entity_frequency_dict):
    entity_list = filter_entity(
        entities_column=entities_column,
        entities_to_keep=set(entity_frequency_dict.keys()),
        field_name='lowercase_value')
    return entity_list


def create_postagging_dict(entities_column):
    entity_postagging_dict = {
        entity_dict['lowercase_value']: entity_dict['postags']
        for entities_list in entities_column for entity_dict in entities_list}
    return entity_postagging_dict


def create_entity_frequency_dict(entities_column, percentage_threshold):
    frequency = dict()
    for entities_list in entities_column:
        entities = map(dict, set(tuple(entity_dict.items()) for
                                 entity_dict in entities_list))
        for entity_dict in entities:
            entity_name = entity_dict['lowercase_value']
            frequency[entity_name] = frequency.get(entity_name, 0) + 1
    sorted_frequencies_lst = sorted(frequency.values(), reverse=True)
    number_items = floor(percentage_threshold * len(frequency))
    threshold_frequency = sorted_frequencies_lst[:number_items][-1]
    delete_low_frequency_entities(threshold_frequency, frequency)
    return frequency


def delete_low_frequency_entities(threshold_frequency, frequency_dict):
    frequency_dict_copy = frequency_dict.copy()

    if threshold_frequency == 1:
        threshold_frequency = 2

    for entity, frequency in frequency_dict_copy.items():
        if frequency < threshold_frequency:
            del frequency_dict[entity]
