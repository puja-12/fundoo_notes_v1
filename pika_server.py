import json
import smtplib

import pika, sys, os


class RabitReceive:

    def send_mail_receive(self, body):

        data = json.loads(body)
        if "url" not in data.keys():
            raise Exception("url not found")
        sender = 'p74174287@gmail.com'
        receivers = [data.get('email')]
        password = "idwuunupswwcnbzt"
        subject = "Verification"
        body = "Click on this " + data.get('url')
        message = f'subject: {subject}\n\n{body}'

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receivers, message)
        except smtplib.SMTPException:
            print("Error: unable to send email")

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='send_mail')

        def callback(ch, method, properties, body):
            self.send_mail_receive(body)
            print(" [x] Received %r" % body)

        channel.basic_consume(queue='send_mail', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


if __name__ == '__main__':
    try:
        RabitReceive().run()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
