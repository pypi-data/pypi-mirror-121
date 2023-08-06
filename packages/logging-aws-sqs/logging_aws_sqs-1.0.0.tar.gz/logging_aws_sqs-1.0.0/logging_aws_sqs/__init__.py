import logging
import logging.handlers

import boto3
from retrying import retry


class AWSSQSHandler(logging.Handler):
    ''' A Python logging handler which sends messages to AWS SQS. '''

    def __init__(self, queue, aws_key_id=None, aws_secret_key=None, aws_region=None, global_param=None):
        '''
        Send log messages to AWS SQS so that messages can be processes downstream
        such as pushing to Splunk for logging.

        : param queue: AWS SQS queue name.
        : param aws_key_id: AWS key ID
        : param aws_secret_key: AWS Secret Key

        Note: Explicit aws_key_id, aws_secret_key is not required if the module is
        used from EC2 role based authentication.
        '''

        logging.Handler.__init__(self)
        sqs = boto3.resource('sqs', aws_access_key_id=aws_key_id,
                             aws_secret_access_key=aws_secret_key, region_name=aws_region)

        # queue = sqs.create_queue(QueueName='test', Attributes={
        #                          'DelaySeconds': '5'})

        self.queue = sqs.get_queue_by_name(QueueName=queue)
        # for queue in sqs.queues.all():
        #     print(queue.url)
        self._global_extra = global_param

        # Since boto3 will also generate logs, which could lead to nested callig, we will disable self logging

        self._entrance_flag = False

    @retry(stop_max_attempt_number=7)
    def emit(self, record):
        '''
        Emit log records by pushing it to AWS SQS queue
        '''

        if self._global_extra is not None:
            record.__dict__.update(self._global_extra)

        if not self._entrance_flag:
            msg = self.format(record)

            self._entrance_flag = True

            try:
                self.queue.send_message(MessageBody=msg)

            finally:
                self._entrance_flag = False
