import datetime
import base64

from TakeBlipInsightExtractor.inputs import models_loader
from TakeBlipInsightExtractor.processing import entity_filter
from TakeBlipInsightExtractor.clustering import embedding, entity_cluster
from TakeBlipInsightExtractor.visualization import entity_hierarchy, word_cloud, csv_file
from TakeBlipMessageStructurer.predict import MessageStructurer


class InsightExtractor:
    def __init__(self, input_data, separator, similarity_threshold,
                 embedding_path, postagging_model_path, postagging_label_path,
                 ner_model_path, ner_label_path, user_email, bot_name, logger):
        self.__logger = logger
        self.__set_entity_cluster(similarity_threshold)
        self.__set_message_structurer(
            postagging_model_path=postagging_model_path,
            postagging_label_path=postagging_label_path, 
            embedding_path=embedding_path,
            ner_model_path=ner_model_path,
            ner_label_path=ner_label_path
        )
        self.__set_output_csv_file(input_data, separator, self.__logger)
        self.__set_output_files_path_dict(user_email, bot_name)
        self.__set_embedding()

    def __set_entity_cluster(self, similarity_threshold):
        self.__logger.log_message('DEBUG', 'Creating cluster layer.')
        self.entity_cluster = entity_cluster.EntityCluster(similarity_threshold)
        self.__logger.log_message('DEBUG', 'Cluster layer created.')

    def __set_message_structurer(self, postagging_model_path,
                                 postagging_label_path, embedding_path,
                                 ner_model_path, ner_label_path):
        self.__logger.log_message('DEBUG', 'Setting Message Structurer.')
        self.__logger.log_message('DEBUG', 'Started reading the PosTagging '
                                           'model.')
        postag_predictor = models_loader.load_postagging_predictor(
            postagging_model_path=postagging_model_path,
            postagging_label_path=postagging_label_path,
            embedding_path=embedding_path
        )
        self.__logger.log_message('DEBUG', 'Finished reading the PosTagging '
                                           'model.')
        
        self.__logger.log_message('DEBUG', 'Started reading the NER model.')   
        ner_predictor = models_loader.load_ner_predictor(
            ner_model_path=ner_model_path,
            ner_label_path=ner_label_path,
            postag_predictor=postag_predictor
        )
        self.__logger.log_message('DEBUG', 'Finished reading the NER model.')
        
        self.__logger.log_message('DEBUG', 'Started Message Structurer '
                                           'creation.')
        self.tags_to_remove = ['INT', 'ART', 'PRON', 'SIMB', 'PON', 'CONJ']
        self.message_structurer = MessageStructurer(
            ner_model=ner_predictor
        )
        self.__logger.log_message('DEBUG', 'Finished Message Structurer '
                                           'creation.')
        self.__logger.log_message('DEBUG', 'Message Structurer set.')

    def __set_output_csv_file(self, input_data, separator, logger=None):
        self.__logger.log_message('DEBUG', 'Setting output csv file.')
        data_from = 'request' if type(input_data) != str else 'file'
        self.output_file = csv_file.OutputFile(
            input_data=input_data,
            encoding='utf-8',
            separator=separator,
            data_from=data_from,
            logger=logger
        )
        self.__logger.log_message('DEBUG', 'Output csv file set.')

    def __set_output_files_path_dict(self, user_email, bot_name):
        self.__logger.log_message('DEBUG', 'Setting Insight Extractor output '
                                           'files names.')
        date = datetime.datetime.now()

        code = '{}_{}_{}{}{}_{}{}{}'.format(
            user_email,
            bot_name,
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second
        )

        code = base64.b64encode(code.encode('ascii')).decode('ascii')

        self.output_files_dict = {
            'word_cloud': 'word_cloud_{}.png'.format(code),
            'entity_hierarchy': 'entity_hierarchy_{}.html'.format(code),
            'output_csv': 'output_{}.csv'.format(code),
            'entity_hierarchy_dict': 'entity_hierarchy_dict_{}.json'
                .format(code)
        }
        self.__logger.log_message('DEBUG', 'Insight Extractor output files '
                                           'names set.')

    def __set_embedding(self):
        self.__logger.log_message('DEBUG', 'Setting embedding.')
        self.embedding = embedding.Embedding(
            self.message_structurer.ner_model.fasttext)
        self.__logger.log_message('DEBUG', 'Embedding set.')

    def predict(self, percentage_threshold, node_messages_examples, batch_size):
        self.__logger.log_message('DEBUG', 'Predict started.')
        self.__structure_messages(batch_size)
        self.__filter_messages(percentage_threshold)
        self.__generate_entities_embedding()
        self.__cluster_messages()
        self.__filter_messages_by_frequency()
        self.__generate_word_cloud()
        self.__generate_entity_hierarchy(node_messages_examples)
        self.__save_files_locally()
        self.__logger.log_message('DEBUG', 'Insight Extractor predict '
                                           'finished.')

    def __structure_messages(self, batch_size):
        self.__logger.log_message('DEBUG', 'Creating Message Structurer '
                                           'column.')
        self.__filtered_message_column, self.__entities_column = self.output_file.\
            create_message_structurer_columns(batch_size,
                                              self.message_structurer,
                                              self.tags_to_remove)
        self.__logger.log_message('DEBUG', 'Message Structurer column '
                                           'created.')

    def __cluster_messages(self):
        self.__logger.log_message('DEBUG', 'Clustering started.')
        self.__create_entity_cluster_dict()
        self.__create_parent_entity_dict()
        self.__create_group_column()
        self.__logger.log_message('DEBUG', 'Clustering finished.')
    
    def __create_entity_cluster_dict(self):
        self.__logger.log_message('DEBUG', 'Creating entity cluster dict.')
        self.__entity_cluster_dict = self.entity_cluster.cluster_entities(
            self.__entities_embedding)
        self.__logger.log_message('DEBUG', 'Entity cluster dict created.')

    def __create_parent_entity_dict(self):
        self.__logger.log_message('DEBUG', 'Creating parent entity dict.')
        self.__parent_entity_dict = entity_hierarchy.create_parent_dict(
            self.__entity_frequency_dict, self.__entity_cluster_dict)
        self.__logger.log_message('DEBUG', 'Parent entity dict created.')

    def __create_group_column(self):
        self.__logger.log_message('DEBUG', 'Creating group column.')
        self.__group_column = self.output_file.create_groups_column(
            self.__entities_column, self.__parent_entity_dict)
        self.__logger.log_message('DEBUG', 'Group column created.')

    def __filter_messages_by_frequency(self):
        self.__logger.log_message('DEBUG', 'Creating filtered messages '
                                           'frequency dict.')
        self.__filtered_messages_frequency_dict = \
            self.output_file.create_filtered_messages_frequency_dict(
                self.__entities_column, self.__filtered_message_column)
        self.__logger.log_message('DEBUG', 'Filtered messages frequency '
                                           'dict created.')

    def __generate_entities_embedding(self):
        self.__logger.log_message('DEBUG', 'Creating entities embedding.')
        self.__entities_embedding = self.embedding.create_entities_embeddings(
            self.__entity_postagging_dict)
        self.__logger.log_message('DEBUG', 'Entities embedding created.')

    def __filter_messages(self, percentage_threshold):
        self.__logger.log_message('DEBUG', 'Creating entities column.')
        self.__entities_column = entity_filter.filter_entity_type(self.__entities_column)
        self.__logger.log_message('DEBUG', 'Entities column created.')

        self.__logger.log_message('DEBUG', 'Creating entity frequency dict.')
        self.__entity_frequency_dict = entity_filter.create_entity_frequency_dict(
            self.__entities_column, percentage_threshold)
        self.__logger.log_message('DEBUG', 'Entity frequency dict created.')
        self.__logger.log_message('DEBUG', '{} entities were found.'
                                  .format(len(self.__entity_frequency_dict)))

        self.__logger.log_message('DEBUG', 'Filtering messages by entities.')
        self.__entities_column = entity_filter.filter_entity_frequency(
            self.__entities_column,self.__entity_frequency_dict)
        self.__logger.log_message('DEBUG', 'Messages filtered.')
        
        self.__logger.log_message('DEBUG', 'Creating entity postagging dict.')
        self.__entity_postagging_dict = entity_filter.create_postagging_dict(
            self.__entities_column)
        self.__logger.log_message('DEBUG', 'Entity postagging dict created.')

    def __generate_word_cloud(self):
        self.__logger.log_message('DEBUG', 'Creating wordcloud image.')
        self.__word_cloud_image = \
            word_cloud.create_word_cloud(self.__entity_frequency_dict,
                                         self.__parent_entity_dict)
        self.__logger.log_message('DEBUG', 'Wordcloud image created.')

    def __generate_entity_hierarchy(self, node_messages_examples):
        self.__logger.log_message('DEBUG', 'Creating entity hierarchy html '
                                           'file.')
        self.__entity_hierarchy_html = entity_hierarchy.create_entity_hierarchy(
            self.__filtered_messages_frequency_dict, self.__parent_entity_dict,
            node_messages_examples)
        self.__logger.log_message('DEBUG', 'Entity hierarchy html file '
                                           'created.')

        self.__logger.log_message('DEBUG', 'Creating entity hierarchy dict '
                                           'file.')
        self.__hierarchy_frequency_dict = entity_hierarchy.create_hierarchy_frequency_dict(
            self.__entity_frequency_dict, self.__parent_entity_dict, self.__group_column)
        self.__logger.log_message('DEBUG', 'Entity hierarchy dict file '
                                           'created.')

    def __save_files_locally(self):
        self.__logger.log_message('DEBUG', 'Saving output file.')
        self.output_file.save_output_file(self.output_files_dict['output_csv'],
                                          self.__filtered_message_column,
                                          self.__entities_column,
                                          self.__group_column)
        self.__logger.log_message('DEBUG', 'Output file saved.')

        self.__logger.log_message('DEBUG', 'Saving wordcloud image.')
        word_cloud.save_word_cloud(self.output_files_dict['word_cloud'],
                                   self.__word_cloud_image)
        self.__logger.log_message('DEBUG', 'Wordcloud image saved.')

        self.__logger.log_message('DEBUG', 'Saving entity hierarchy html '
                                           'file.')
        entity_hierarchy.save_entity_hierarchy(
            self.output_files_dict['entity_hierarchy'],
            self.__entity_hierarchy_html)
        self.__logger.log_message('DEBUG', 'Entity hierarchy html file saved.')

        self.__logger.log_message('DEBUG', 'Saving entity hierarchy dict '
                                           'file.')
        entity_hierarchy.save_entity_hierarchy_dict(
            self.output_files_dict['entity_hierarchy_dict'],
            self.__hierarchy_frequency_dict)
        self.__logger.log_message('DEBUG', 'Entity hierarchy dict file saved.')
