import json
import uuid
import socket
import logging
from pytz import timezone
from datetime import datetime
from azure.eventhub import EventData
from azure.eventhub import EventHubProducerClient


class EventHubLogSender():
    """Sends logs to EventHub.

     Methods:
      * log_message - Sends log to EventHub.
      * log_error_message - Logs error messages and sends it to EventHub.
      * generate_json_log - Generates log in JSON format.
      * generate_json_log_to_print - Generates log in printable format.
    """

    def __init__(
            self,
            application_name: str,
            user_email: str,
            bot_name: str,
            file_name: str,
            correlation_id: str,
            connection_string: str = None,
            eventhub_name: str = None) -> None:
        """
        :param application_name: Running application name.
        :type application_name: `str`
        :param user_email: Email from the user sending the request.
        :type user_email: `str`
        :param bot_name: Name of the bot being analyzed. 
        :type bot_name: `str`
        :param file_name: Name of the file being analyzed.
        :type file_name: `str`
        :param correlation_id: Execution unique id.
        :type correlation_id: `str` of `uuid`
        :param connection_string: Eventhub's connection string.
        :type connection_string: `str`
        :param eventhub_name: Name of the log event hub.
        :type eventhub_name: `str`
        """
        self.__connection_string = connection_string
        self.__eventhub_name = eventhub_name
        self.__application_name = application_name
        self.__user_email = user_email
        self.__bot_name = bot_name
        self.__file_name = file_name
        self.__correlation_id = correlation_id
        self.__timezone = timezone('Brazil/East')
        self.__connect_to_eventhub()
        self.__generate_level_dict()
        logging.getLogger("uamqp").setLevel(logging.CRITICAL)
        logging.getLogger("azure.eventhub").setLevel(logging.CRITICAL)

    def __connect_to_eventhub(self) -> None:
        if self.__eventhub_is_initialized():
            self.__sender = EventHubProducerClient.from_connection_string(
                conn_str=self.__connection_string,
                eventhub_name=self.__eventhub_name)
            self.__event_batch = self.__sender.create_batch()

    def __eventhub_is_initialized(self) -> bool:
        return self.__eventhub_name and self.__connection_string

    def __generate_level_dict(self) -> None:
        self.__level_dict = {
            'DEBUG': 10,
            'INFO': 20,
            'WARNING': 30,
            'ERROR': 40,
            'CRITICAL': 50
        }

    def log_message(self, level: str, message: str) -> None:
        """Sends log to EventHub.

        :param level: Criticity level. 
            Can either be of "DEBUG", "INFO", "WARNING", 
            "ERROR" or "CRITICAL". 
        :type level: `str`
        :param message: Message informing the event.
        :type message: `str`
        """
        self.__connect_to_eventhub()
        self.__send_message_to_eventhub(level, message)

    def log_error_message(self, level: str, message: str) -> None:
        """Logs error messages and sends it to EventHub.

        :param level: Criticity level. 
            Can either be of "DEBUG", "INFO", "WARNING", 
            "ERROR" or "CRITICAL". 
        :type level: `str`
        :param message: Message informing the event.
        :type message: `str`
        """
        logging.error(message)
        self.__connect_to_eventhub()
        self.__send_message_to_eventhub(level, message)

    def __send_message_to_eventhub(self, level: str, message: str) -> None:
        timestamp = str(datetime.now(self.__timezone))

        self.generate_json_log(timestamp, level, message)
        print(self.generate_json_log_to_print(timestamp, level, message))

        if self.__eventhub_is_initialized():
            with self.__sender:
                self.__event_batch.add(EventData(self.json_log))
                self.__sender.send_batch(self.__event_batch)

    def generate_json_log(
            self,
            timestamp: str,
            level: str,
            message: str) -> None:
        """Generates log in JSON format.

        :param timestamp: When the log happened.
        :type timestamp: `str`
        :param level: Criticity level. 
            Can either be of "DEBUG", "INFO", "WARNING", 
            "ERROR" or "CRITICAL". 
        :type level: `str`
        :param message: Message informing the event.
        :type message: `str`
        """
        log_id = str(
            uuid.uuid3(
                uuid.NAMESPACE_DNS,
                self.__user_email + self.__bot_name + timestamp))

        extras = {
            'UserEmail': self.__user_email,
            'BotName': self.__bot_name,
            'FileName': self.__file_name,
            'HostName': socket.gethostname(),
        }

        self.json_log = json.dumps({
            'StorageDateBR': timestamp,
            'CorrelationId': self.__correlation_id,
            'Id': log_id,
            'Application': self.__application_name,
            'Level': level,
            'Message': message,
            'Extras': extras
        })

    def generate_json_log_to_print(
            self,
            timestamp: str,
            level: str,
            message: str) -> str:
        """Generates log in printable format.

        :param timestamp: When the log happened.
        :type timestamp: `str`
        :param level: Criticity level. 
            Can either be of "DEBUG", "INFO", "WARNING", 
            "ERROR" or "CRITICAL". 
        :type level: `str`
        :param message: Message informing the event.
        :type message: `str`
        :return: Log in printable format
        :rtype: `str`
        """

        return '{} : {} : {} : {} : {} : {} : {} : {}'.format(
            level,
            timestamp,
            self.__correlation_id,
            self.__application_name,
            socket.gethostname(),
            self.__user_email,
            self.__bot_name,
            message)
