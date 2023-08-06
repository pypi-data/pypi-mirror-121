from flask import Flask

from GitHook import Webhook
from GitHook.events import Push_Event, Release_Event

if __name__ == '__main__':
    app = Flask(__name__)

    webhook = Webhook(app)

    @webhook.hook('/github', Push_Event)
    def on_push(event: Push_Event):
        print(f'GOT A PUSH')

    @webhook.hook('/github', Release_Event)
    def on_release(event: Release_Event):
        pass
