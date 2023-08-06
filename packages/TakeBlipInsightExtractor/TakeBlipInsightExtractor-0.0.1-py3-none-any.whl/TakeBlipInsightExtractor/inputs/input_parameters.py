import os
import re

def get_ie_static_parameters():
    return {
        'node_messages_examples': get_node_messages_examples(),
        'similarity_threshold': get_similarity_threshold(),
        'percentage_threshold': get_percentage_threshold(),
        'batch_size': get_batch_size(),
        'chunk_size': get_chunk_size(),
        'embedding_path': get_embedding_path(),
        'postagging_model_path': get_postagging_model_path(),
        'postagging_label_path': get_postagging_label_path(),
        'ner_model_path': get_ner_model_path(),
        'ner_label_path': get_ner_label_path(),
        'eventhub_name': get_eventhub_name(),
        'application_name': get_application_name()
    }

def get_embedding_path():
    return get_azureml_file_path(
        env_model_name='EMBEDDING_VERSION',
        env_full_name='EMBEDDING_FULL_NAME',
        env_registry_name='EMBEDDING_REGISTRY_NAME'
    )

def get_postagging_model_path():
    return get_azureml_file_path(
        env_model_name='POSTAGGING_VERSION',
        env_full_name='POSTAGGING_FULL_NAME',
        env_registry_name='POSTAGGING_REGISTRY_NAME'
    )

def get_postagging_label_path():
    return get_azureml_file_path(
        env_model_name='POSTAGGING_LABEL_VERSION',
        env_full_name='POSTAGGING_LABEL_FULL_NAME',
        env_registry_name='POSTAGGING_LABEL_REGISTRY_NAME'
    )

def get_ner_model_path():
    return get_azureml_file_path(
        env_model_name='NER_VERSION',
        env_full_name='NER_FULL_NAME',
        env_registry_name='NER_REGISTRY_NAME'
    )

def get_ner_label_path():
    return get_azureml_file_path(
        env_model_name='NER_LABEL_VERSION',
        env_full_name='NER_LABEL_FULL_NAME',
        env_registry_name='NER_LABEL_REGISTRY_NAME'
    )

def get_azureml_file_path(env_model_name, env_full_name, env_registry_name):
    azureml_dir = os.environ.get('AZUREML_MODEL_DIR')
    file_version = os.environ.get(env_model_name)
    file_full_name = os.environ.get(env_full_name)
    file_registry_name = os.environ.get(env_registry_name)
    return os.path.join(
        azureml_dir,
        file_registry_name,
        file_version,
        file_full_name
    )

def get_node_messages_examples():
    return int(os.environ.get('NUMBER_NODE_MESSAGES_EXAMPLES', 6))

def get_similarity_threshold():
    return float(os.environ.get('SIMILARITY_THRESHOLD', 0.65))

def get_percentage_threshold():
    return float(os.environ.get('PERCENTAGE_THRESHOLD', 0.7))

def get_batch_size():
    return int(os.environ.get('BATCH_SIZE', 50))

def get_chunk_size():
    return int(os.environ.get('CHUNK_SIZE', 1024))

def get_environment():
    return os.environ.get('ENVIRONMENT', 'prod')

def get_eventhub_name():
    return os.environ.get('EVENTHUB_NAME', None)

def get_application_name():
    return os.environ.get('APPLICATION_NAME', None)

def get_parameters(multipart_data):
    parameters = {
        'separator': '|',
        'file_name': 'file.csv',
        'bot_name' : None,
        'user_email': None,
        'file': None,
    }
    for part in multipart_data.parts:
        disposition = part.headers[b'Content-Disposition'].decode('utf-8')
        parameter_name = re.search('name="(.*?)"', disposition.split(';')[1]).group(1)
        if parameter_name == 'bot_name':
            parameters['bot_name'] = part.text
        elif parameter_name == 'user_email':
            parameters['user_email'] = part.text
        elif parameter_name == 'separator':
            parameters['separator'] = part.text
        elif parameter_name == 'file':
            parameters['file'] = part
            parameters['file_name'] = re.search('filename="(.*?)"', disposition.split(';')[2]).group(1)
    return parameters

def check_parameters(parameters):
    for parameter_name in parameters:
        if not parameter_name:
            raise ValueError('Missing {} parameter in form data request'.format(parameter_name))