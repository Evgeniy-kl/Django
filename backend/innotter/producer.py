import json

from innotter.services import RabbitManage


def pusblish(body):
    rabbit_obj = RabbitManage('moose.rmq.cloudamqp.com',
                              5672,
                              'nzocntbp',
                              'nzocntbp',
                              'bLDWuRiZsMh96jL2d0yCAiMvvWtBvpTr')

    channel = rabbit_obj.connect()

    channel.exchange_declare('django_exchange')
    channel.queue_declare(queue='django_queue')
    channel.queue_bind('django_queue', 'django_exchange', 'tests')
    channel.basic_publish(
        body=json.dumps(body),
        exchange='django_exchange',
        routing_key='tests',
    )
    channel.close()

    print('Message sent')
