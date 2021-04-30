import logging
import random
import time
from jaeger_client import Config

if __name__ == "__main__":
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)

    config = Config(
        config={ # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name='sample-jaeger',
        validate=True,
    )
    # this call also sets opentracing.tracer
    tracer = config.initialize_tracer()

    with tracer.start_span('TestSpan') as span:
        span.log_kv({'event': 'test message', 'life': 42})

        with tracer.start_span('ChildSpan', child_of=span) as child_span:
            child_span.log_kv({'event': 'down below'})

    time.sleep(2)   # yield to IOLoop to flush the spans - https://github.com/jaegertracing/jaeger-client-python/issues/50
    tracer.close()  # flush any buffered spans

# Log generation application
# The goal of this application is to semi randomly generate logs that which will be passed on to the Jaeger agent by the Jaeger client

# Types of log ids
log_ids = [
    "1001",
    "1002",
    "1003",
    "1004",
    "1005"
]

# Log messages
log_messages = [
    "Sample message 1",
    "Sample message 2",
    "Sample message 3",
    "Sample message 4",
    "Sample message 5",
    "Sample message 6",
    "Sample message 7",
    "Sample message 8",
    "Sample message 9",
    "Sample message 10"
]

def log_generation(percent_anom):
    anom = ""
    # Choose whether the log is anomalous or not
    if (random.randint(1, 100) <= percent_anom):
        anom = "Warning: "

    # Choose a log id
    log_id_index = random.randint(0, 4)
    log_id = log_ids[log_id_index]
    # Choose a time for the log
    log_hour = str(random.randint(1, 12))
    log_min = str(random.randint(0, 59))
    log_sec = str(random.randint(0, 59))
    # Choose a message
    log_message_index = random.randint(0, 9)
    log_message = log_messages[log_message_index]

    log = log_id + " " + log_hour + ":" + log_min + ":" + log_sec + " " + anom + log_message
    print(log)

# Loop
while (True):
    log_generation(5)