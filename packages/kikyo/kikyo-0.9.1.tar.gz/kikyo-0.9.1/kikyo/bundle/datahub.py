import datetime as dt
import io
import json
import pickle
from typing import Any

import pulsar
from _pulsar import ConsumerType, InitialPosition
from fastavro import parse_schema, schemaless_writer, schemaless_reader

from kikyo import Kikyo
from kikyo.datahub import DataHub, Producer, Consumer, Message

record_schema = {
    'name': 'DataHubRecord',
    'namespace': 'kikyo.datahub',
    'type': 'record',
    'fields': [
        {'name': 'type', 'type': 'string'},
        {'name': 'data', 'type': 'bytes'}
    ]
}

parsed_record_schema = parse_schema(record_schema)


class PulsarBasedDataHub(DataHub):
    def __init__(self, client: Kikyo):
        settings = client.settings.deep('pulsar')
        if not settings:
            return

        self.tenant = settings.get('tenant', 'public')
        self.namespace = settings.get('namespace', 'default')
        self.pulsar = pulsar.Client(settings['service_url'])

        client.add_component('pulsar_datahub', self)

    def create_producer(self, topic: str) -> Producer:
        return PulsarBasedProducer(self, topic)

    def subscribe(self, topic: str, subscription_name: str = None, auto_ack: bool = True) -> Consumer:
        return PulsarBasedConsumer(self, topic, subscription_name=subscription_name)

    def get_topic(self, name: str):
        return f'persistent://{self.tenant}/{self.namespace}/{name}'


class PulsarBasedProducer(Producer):
    def __init__(self, datahub: PulsarBasedDataHub, topic: str):
        super().__init__()
        self.producer = datahub.pulsar.create_producer(
            datahub.get_topic(topic),
            block_if_queue_full=True,
        )

    def send(self, *records: Any):
        for record in records:
            data = MessageWrapper(record).build()
            self.producer.send_async(data, callback=self.callback)
        self.producer.flush()

    def close(self):
        self.producer.close()

    def callback(self, res, msg_id):
        pass


class PulsarMessage(Message):
    def __init__(self, msg):
        self._msg = msg
        self._value = MessageWrapper.extract_data(msg.data())

    @property
    def value(self) -> Any:
        return self._value


class PulsarBasedConsumer(Consumer):
    def __init__(
            self,
            datahub: PulsarBasedDataHub,
            topic: str, subscription_name: str = None,
            auto_ack: bool = True,
    ):
        super().__init__()
        self.consumer = datahub.pulsar.subscribe(
            datahub.get_topic(topic),
            consumer_type=ConsumerType.KeyShared,
            subscription_name=subscription_name,
            initial_position=InitialPosition.Earliest,
        )
        self._auto_ack = auto_ack

    def receive(self) -> Message:
        msg = self.consumer.receive()
        if self._auto_ack:
            self.consumer.acknowledge(msg)
        return PulsarMessage(msg)

    def close(self):
        self.consumer.close()

    def ack(self, msg: Message):
        assert isinstance(msg, PulsarMessage)
        self.consumer.acknowledge(msg._msg)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dt.datetime):
            return obj.isoformat()
        elif isinstance(obj, dt.date):
            return obj.isoformat()
        return super().default(o)


class MessageWrapper:
    ENCODING = 'utf-8'

    def __init__(self, data: Any):
        self.type = None
        self.data = None
        if isinstance(data, (dict, list)):
            self.type = 'json'
            self.data = json.dumps(
                data,
                ensure_ascii=False,
                cls=JSONEncoder,
            ).encode(encoding=self.ENCODING)
        elif isinstance(data, bytes):
            self.type = 'bytes'
            self.data = data
        elif isinstance(data, str):
            self.type = 'str'
            self.data = data.encode(encoding=self.ENCODING)
        else:
            self.type = 'object'
            self.data = pickle.dumps(data)

    def build(self) -> bytes:
        d = {
            'type': self.type,
            'data': self.data
        }
        wio = io.BytesIO()
        schemaless_writer(wio, parsed_record_schema, d)
        return wio.getvalue()

    @classmethod
    def extract_data(cls, content: bytes) -> Any:
        message = schemaless_reader(io.BytesIO(content), parsed_record_schema)
        if message['type'] == 'json':
            return json.loads(message['data'].decode(encoding=cls.ENCODING))
        if message['type'] == 'bytes':
            return message['data']
        if message['type'] == 'str':
            return message['data'].decode(encoding=cls.ENCODING)
        if message['type'] == 'object':
            return pickle.loads(message['data'])
