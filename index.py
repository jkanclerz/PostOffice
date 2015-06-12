#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import json
import config
import pika

credentials = pika.PlainCredentials(config.RABBIT_USER, config.RABBIT_PASS)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        config.RABBIT_IP,
        config.RABBIT_PORT,
        '/',
        credentials
   )
)
# Setup Flask
app = Flask(__name__)

@app.route("/")
def index():
  my_name = 'Jakub'
  return render_template('partials/index.html',
    my_name=my_name,
  )

@app.route("/send", methods=['POST'])
def send():
  my_name = 'Jakub'
  email = request.form.get('email')
  content = request.form.get('content')

  emailInfo = {'email': email, 'content': content}
  dispatchMQMessage(emailInfo)

  return redirect(url_for('index'))

def dispatchMQMessage(emailObject):
  channel = connection.channel()
  channel.queue_declare(queue=config.RABBIT_EMAIL_QUEUE)

  message = json.dumps(emailObject)

  channel.basic_publish(
      exchange='',
      routing_key=config.RABBIT_EMAIL_QUEUE,
      body=message
  )
  return


if __name__ == "__main__":
  app.run(debug=True, host='192.168.33.40')
