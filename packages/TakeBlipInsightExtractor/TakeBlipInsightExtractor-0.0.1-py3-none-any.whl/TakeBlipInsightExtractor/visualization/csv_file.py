import csv


class DataGenerator:
    def __init__(self, data, separator):
        self.data = data
        self.separator = separator

    @classmethod
    def from_multipart_data_request(cls, part_data, encoding, separator):
        file_part_data = part_data.text.splitlines()
        return cls(file_part_data, separator)

    @classmethod
    def from_file_data(cls, path, encoding, separator):
        file_handler = open(path, encoding=encoding)
        return cls(file_handler, separator)

    def iterate_data(self):
        csv_reader = csv.reader(self.data, delimiter=self.separator)
        for row in csv_reader:
            yield row


class OutputFile:
    def __init__(self, input_data, encoding, separator, data_from='request',
                 logger=None):
        self.input_data = input_data
        self.encoding = encoding
        self.separator = separator
        self.__logger = logger
        self.get_data = self.get_data_from_request if data_from == 'request' \
            else self.get_data_from_file
        self.__set_header()
    
    def get_data_from_file(self):
        return DataGenerator.from_file_data(
            path=self.input_data,
            encoding=self.encoding,
            separator=self.separator
        ).iterate_data()
        
    def get_data_from_request(self):
        return DataGenerator.from_multipart_data_request(
            part_data=self.input_data,
            encoding=self.encoding,
            separator=self.separator
        ).iterate_data()

    def __set_header(self):
        self.header = ['Message', 'Entities', 'Groups', 'Structured Message']

    def parse_message_structurer_content(self, structured_messages_list):
        filtered_message_column = []
        entities_column = []
        for structured_message in structured_messages_list:
            filtered_message_column.append(
                structured_message['lowercase_filtered_message'])
            content = structured_message['content']
            if len(content) > 0:
                entities_list = [tag for tag in content
                                 if tag['type'] != 'postagging']
            else:
                entities_list = []
            entities_column.append(entities_list)
        return filtered_message_column, entities_column

    def create_message_structurer_columns(self, batch_size,
                                          message_structurer, tags_to_remove):
        ms_input_batch = [{'id': ind, 'sentence': row[0]} for ind, row in
                          enumerate(self.get_data())]
        
        self.log_message('DEBUG', 'Number of messages sent to be '
                                  'structured {}.'
                         .format(len(ms_input_batch)))
        self.log_message('DEBUG', 'Maximum message size {}'
                         .format(max(len(message['sentence'].split())
                                     for message in ms_input_batch)))

        structured_messages_list = sorted(
            message_structurer.structure_message_batch(
                batch_size=batch_size,
                sentences=ms_input_batch,
                tags_to_remove=tags_to_remove
            ),
            key=lambda content_dict: content_dict['id']
        )
        self.log_message('DEBUG', 'Messages structured with success.')
        filtered_message_column, entities_column = \
            self.parse_message_structurer_content(structured_messages_list)
        return filtered_message_column, entities_column
    
    def log_message(self, level, message):
        if self.__logger: 
            self.__logger.log_message(level, message)

    def create_groups_column(self, entities_column, parent_entity_dict):
        group_column = []
        entity_parent_dict = {child: parent for parent, children_lst in
                              parent_entity_dict.items() for child in
                              children_lst}

        for entities_list in entities_column:
            temp_list = []
            for entity_dict in entities_list:
                entity_name = entity_dict['lowercase_value']
                parent = entity_parent_dict[entity_name]
                temp_list.append(parent)
            group_column.append(temp_list)
        return group_column

    def create_filtered_messages_frequency_dict(self, entities_column,
                                                filtered_message_column):
        filtered_messages_frequency_dict = {}
        entity_filtered_message_dict = {}
        for filtered_message in filtered_message_column:
            filtered_messages_frequency_dict[
                filtered_message] = filtered_messages_frequency_dict.get(
                filtered_message, 0) + 1

        for filtered_message, entities_list in zip(filtered_message_column,
                                                   entities_column):
            for entity_dict in entities_list:
                entity_name = entity_dict['lowercase_value']
                if entity_filtered_message_dict.get(entity_name) is not None:
                    entity_filtered_message_dict[entity_name].append((
                        filtered_message,
                        filtered_messages_frequency_dict[filtered_message]))
                    entity_filtered_message_dict[entity_name] = list(
                        set(entity_filtered_message_dict[entity_name]))
                else:
                    entity_filtered_message_dict[entity_name] = [(
                        filtered_message, filtered_messages_frequency_dict[
                            filtered_message])]
        return entity_filtered_message_dict

    def __generate_output_file(self, filtered_message_column,
                               entities_column, group_column):
        for message, entity, group, filtered_message in zip(
                                                            self.get_data(),
                                                            entities_column,
                                                            group_column,
                                                            filtered_message_column):
            yield message[0], entity, group, filtered_message

    def save_output_file(self, full_path, filtered_message_column,
                         entities_column, group_column):
        with open(full_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=self.separator)
            if self.header:
                writer.writerow(self.header)
            for row in self.__generate_output_file(filtered_message_column,
                                                   entities_column,
                                                   group_column):
                writer.writerow(row)
