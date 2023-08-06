import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender():
    def __init__(self):
        self.sender = 'insightextractor.dataanalytics@gmail.com'
        self.username = self.sender
        self.__password = self.__get_password_from_env()
        self.subject = 'Insight Extractor - Processamento Finalizado'
        self.host = 'smtp.gmail.com'
        self.port = 587

    def __get_password_from_env(self):
        env_variable_name = 'EMAIL_PASSWORD'
        password = os.environ[env_variable_name]
        return password

    def create_email_text(self, files_url_dict, elapsed_minutes, file_name):
        email_text = '''
            Para as frases enviadas no arquivo {}, foram encontradas diferentes entidades,
            as quais foram agrupadas conforme a imagem com a nuvem de entidades ({}). 
            Nesse arquivo, as cores indicam o grupo de entidades e o tamanho é proporcional a frequência de vezes
            que essa entidade apareceu nas mensagens. O agrupamento das entidades está no arquivo de hierarquia entidades ({}).
            Similarmente, o arquivo json ({}) mostra tópicos relacionados às entidades com hierarquia.
            Mais detalhes com as frases para cada entidade podem ser vistas no arquivo csv
            que contém as informações para cada mensagem ({}).
            Tempo de processamento: {:.2f} minutos
        '''.format(
            file_name,
            files_url_dict['word_cloud'],
            files_url_dict['entity_hierarchy'],
            files_url_dict['entity_hierarchy_dict'],
            files_url_dict['output_csv'],
            elapsed_minutes
        )
        return email_text

    def send_email(self, user_email, email_text, logger):
        self.__logger = logger
        self.__set_destination_emails(user_email, email_text)
        self.__connect_to_server()
        self.__dispatch_email(user_email)
        self.__disconnect_from_server()
        

    def __set_destination_emails(self, user_email, email_text):
        try:
            self.__logger.log_message('DEBUG','Setting email addresses.')
            recipients = [user_email, 'analytics.dar@take.net']
            self.msg = MIMEMultipart()
            self.msg['From'] = self.sender
            self.msg['To'] = ', '.join(recipients)
            self.msg['Subject'] = self.subject
            self.msg.attach(MIMEText(email_text))
            self.__logger.log_message('DEBUG','Email addresses set.')
        except (Exception) as e:
            self.__logger.log_error_message('ERROR', 'Error {} while setting email addresses!'.format(e))

    def __connect_to_server(self):
        try:
            self.__logger.log_message('DEBUG','Started server connection.')
            self.smtp = smtplib.SMTP(host=self.host, port=self.port) 
            self.smtp.starttls()
            self.smtp.login(self.username, self.__password)
            self.__logger.log_message('DEBUG','Email server connected successfully.')
        except (Exception) as e:
            self.__logger.log_error_message('ERROR', 'Error {} connecting to email server!'.format(e))

    def __dispatch_email(self, user_email):
        try:
            self.__logger.log_message('DEBUG','Sending email.')
            self.smtp.sendmail(self.sender, user_email, self.msg.as_string())
            self.__logger.log_message('DEBUG','Email sent successfully.')
        except (Exception) as e:
            self.__logger.log_error_message('ERROR', 'Error {} while sending email!'.format(e))

    def __disconnect_from_server(self):
        try:
            self.smtp.close()
            self.__logger.log_message('DEBUG','Email server connection closed.')
        except (Exception) as e:
            self.__logger.log_error_message('ERROR', 'Error {} while closing connection to email server!'.format(e))