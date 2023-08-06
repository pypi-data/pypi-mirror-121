def get_response_message(file_name, user_email):
    response_message = (
        'Recebemos a sua requisição para o arquivo {} e dentro '
        'de alguns minutos enviaremos para o e-mail {} passado.'
    ).format(file_name, user_email)
    return response_message