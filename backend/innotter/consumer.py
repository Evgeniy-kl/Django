import pika

credentials = pika.PlainCredentials('nzocntbp', 'bLDWuRiZsMh96jL2d0yCAiMvvWtBvpTr')
parameters = pika.ConnectionParameters('moose.rmq.cloudamqp.com',
                                       5672,
                                       'nzocntbp',
                                       credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='fastapi_queue')


def callback(ch, method, properties, body):
    print(f'Received: {body}')


channel.basic_consume(queue='fastapi_queue', on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()
