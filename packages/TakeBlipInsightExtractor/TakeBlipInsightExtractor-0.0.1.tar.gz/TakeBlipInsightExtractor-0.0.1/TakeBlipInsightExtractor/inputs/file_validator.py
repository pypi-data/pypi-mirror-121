import time
import logging


class FileValidator:
    """Analyze whether the file is valid.
    
     Methods:
      * is_valid_file - Return `True` if file passes all validations, `False` otherwise.
      * has_valid_encoding - Return `True` if file has valid encoding, `False` otherwise.
      * has_valid_extension - Return `True` if file has valid extension, `False` otherwise.
      * has_empty_lines - Return `True` if file has empty lines, `False` otherwise.
      * get_error_message - Return message with found file errors.
    """

    def __init__(
        self, 
        encoding: str, 
        extension: str, 
        file_content: bytes, 
        file_name: str = 'file_name', 
        logger=None) -> None:
        """ 
        :param encoding: Correct file encoding.
        :type encoding: `str`
        :param extension: Correct file extension.
        :type extension: `str`
        :param file_content: File content.
        :type file_content: `bytes`
        :param file_name: File name.
        :type file_name: `str`
        :param logger: Object to log class activities.
        :type logger: `None`
        """
        self.__encoding = encoding
        self.__extension = extension
        self.__error_message = []
        self.__logger = logger
        self.__file_content = file_content
        self.__file_name = file_name

    def is_valid_file(self) -> bool:
        """Return `True` if file passes all validations, `False` otherwise.

        :return: `True` if file passes all validations, `False` otherwise.
        :rtype: `bool`
        """
        start_time = time.time()
        is_valid_file = all([
            self.has_valid_encoding(),
            self.has_valid_extension(),
            not self.has_empty_lines()
        ])
        self.__log('Time elapsed to validate file {} seconds'.format(time.time() - start_time))
        return is_valid_file

    def has_valid_encoding(self) -> bool:
        """Return `True` if file has valid encoding, `False` otherwise.

        :return: `True` if file has valid encoding, `False` otherwise.
        :rtype: `bool`
        """
        try:
            decoded_data = self.__file_content.strip().decode(self.__encoding)
            return True
        except UnicodeDecodeError as e:
            self.__error_message.append('Encoding inválido')
            self.__log_error(self.__error_message)
            return False

    def has_valid_extension(self) -> bool:
        """Return `True` if file has valid extension, `False` otherwise.

        :return: `True` if file has valid extension, `False` otherwise.
        :rtype: `bool`
        """
        file_type = self.__file_name.split('.')[-1]
        if self.__extension not in file_type:
            self.__error_message.append('Extensão inválida')
            self.__log_error(self.__error_message)
            return False
        return True

    def has_empty_lines(self) -> bool:
        """Return `True` if file has empty lines, `False` otherwise.
        
        :return: `True` if file has empty lines, `False` otherwise.
        :rtype: `bool`
        """
        try:
            empty_lines = sum(len(line.strip()) == 0 for line in self.__file_content.splitlines())
            if empty_lines == 0:
                return False
            self.__error_message.append('Linha em branco')
            self.__log_error(self.__error_message)
            return True
        except UnicodeDecodeError as e:
            self.__log_error(e)
            return True

    def get_error_message(self) -> str:
        """Return message with found file errors. 
        
        :return: message with found file errors.
        :rtype: `str`
        """
        found_errors = ' ; '.join(self.__error_message)
        return f'Sua requisição não será processada. Arquivo enviado possui o(s) seguinte(s) erro(s): {found_errors}'

    def __log_error(self, message: str) -> None:
        if self.__logger:
            self.__logger.log_error_message('ERROR', message)

    def __log(self, message: str) -> None:
        if self.__logger:
            self.__logger.log_message('DEBUG', message)
