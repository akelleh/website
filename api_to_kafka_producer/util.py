import tornado.gen
import logging
import confluent_kafka
import boto3
import config


conf = {
    'bootstrap.servers': f"{config.kafka['ip']}:{config.kafka['port']}",
}
kafka = confluent_kafka.Producer(**conf)

@tornado.gen.coroutine
def pub(message):
    kafka.produce(config.kafka['topic'],
                  value=message)
    kafka.flush(timeout=1.)
    logging.info("message published.")

def send_sms(message, phone_number):
    sns = boto3.client('sns', region_name='us-east-1')
    response = sns.publish(
        PhoneNumber=phone_number,
        Message=message,
    )
    logging.info(f"SMS response: {response}")
