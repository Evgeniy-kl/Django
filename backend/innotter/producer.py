import pika, json


def pusblish(body):
    credentials = pika.PlainCredentials('nzocntbp', 'bLDWuRiZsMh96jL2d0yCAiMvvWtBvpTr')
    parameters = pika.ConnectionParameters('moose.rmq.cloudamqp.com',
                                           5672,
                                           'nzocntbp',
                                           credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.exchange_declare('django_exchange')
    channel.queue_declare(queue='django_queue')
    channel.queue_bind('django_queue', 'django_exchange', 'tests')
    channel.basic_publish(
        body=json.dumps(body),
        exchange='django_exchange',
        routing_key='tests',
    )
    channel.close()
    connection.close()
    print('Message sent')
