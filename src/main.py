from dotenv import load_dotenv
from src.infrastructure.runner.runner import Runner
from src.infrastructure.queue.queue import Queue
from src.infrastructure.mail.mail import Mail

from src.domain import ContactInfoHandler

load_dotenv()


def create_runner():
    queue_service = Queue()
    mail = Mail()
    handler = ContactInfoHandler(mail=mail)

    return Runner(
        queue_service=queue_service,
        handler=handler
    )


if __name__ == "__main__":
    load_dotenv()
    runner = create_runner()
    print('- WORKER STARTED -')
    print(f'Listening for messages on {runner.queue_service.queue_url}')
    while True:
        runner.process()
