import os
import re
import uuid
import logging
import datetime
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, BlobBlock

class Storage:
    def __init__(self, environment):
        self.environment = environment
        self.__set_blob_service_client(environment)

    def __get_connection_string(self):
        env_variable_name = 'HMG_STORAGE_CONNECTION_STRING' if self.environment == 'hmg' else 'STORAGE_CONNECTION_STRING'
        connection_string = os.environ[env_variable_name]
        return connection_string
        
    def __set_blob_service_client(self, environment):
        self.blob_service_client = BlobServiceClient.from_connection_string(
            conn_str=self.__get_connection_string()
        )
        
    def __get_blob_client(self, user_container_name, directory_name, file_path):
        blob_client = BlobClient.from_connection_string(
            conn_str=self.__get_connection_string(),
            container_name=user_container_name,
            blob_name=os.path.join(directory_name, file_path)
        )
        return blob_client
    
    def __get_directory_name(self, bot_name):
        date = datetime.datetime.now() 
        directory_name = '{}_{}{}{}_{}{}{}'.format(
            bot_name,
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second
        )
        return directory_name 
    
    def __upload_file(self, file_path, blob_client, chunk_size, logger):
        logging.disable(logging.INFO)
        block_list = []
        try:
            logger.log_message('DEBUG','Uploading {}'.format(file_path))
            with open(file_path, "rb") as f:
                while True:
                    read_data = f.read(chunk_size)
                    if not read_data:
                        break
                    blk_id = str(uuid.uuid4())
                    blob_client.stage_block(block_id=blk_id,data=read_data) 
                    block_list.append(BlobBlock(block_id=blk_id))
            blob_client.commit_block_list(block_list)
            logger.log_message('DEBUG','{} uploaded'.format(file_path))
        except Exception as e:
            logger.log_error_message('ERROR', 'Error {} while uploading file {}'.format(e, file_path))
            
    def create_user_container(self, user_email, logger):
        user_container_name = re.search('(.*?)@take.net', user_email).group(1).replace('.','')
        try:
            self.blob_service_client.create_container(
                name=user_container_name,
                public_access='Blob'
            )
        except ResourceExistsError:
            logger.log_message('DEBUG','Container for user {} already exists'.format(user_container_name))
        except Exception as e:
            logger.log_error_message('ERROR', 'Error {} while creating user container.'.format(e))
        else:
            logger.log_message('DEBUG','Created container for user {}'.format(user_container_name))
        finally:
            return user_container_name

    def save_files_to_storage(self, save_files_dict, user_container_name, bot_name, chunk_size, logger):
        files_url_dict = {}
        directory_name = self.__get_directory_name(bot_name)
        for file_name, file_path in save_files_dict.items():
            blob_client = self.__get_blob_client(user_container_name, directory_name, file_path)
            files_url_dict[file_name] = blob_client.url
            self.__upload_file(file_path, blob_client, chunk_size, logger)
        return files_url_dict