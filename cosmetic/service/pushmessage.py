from flask import Blueprint
from flask.json import jsonify
from firebase_admin import messaging

import os
import firebase_admin

from firebase_admin import credentials

cred_path = os.path.join("cosmetic/data/", "serviceAccountKey.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

SERVER_API_KEY = "AAAA82vbQso:APA91bGoMlx434BzWaxeF5xQmUKOnXOz7LpWfOCLXZ7vyWMYkFTQufkfKAleBbzFlYI92Ru1hLsvyKUNf49Akqkr0hPqvZs-asGze15DGOtQv3-S080rvXRDrTjev_FsUHCE0eaP63KG"
SENDER_ID = "1045486584522"
bp = Blueprint('pushmessage', __name__, url_prefix='/pushmessage')

@bp.route('/real', methods=["GET"])
def test():
    A1 = "cydhF1U6RcOFNafwNqz7xJ:APA91bFnDCXl10JmqL2fsnFqNSpJvW4FYibaANWqF2J2Fk2idurz8cgnvxseiG2VBmtDnzpwI1XszQLwRkon6IsztvYBtyY3Dukc5SwjYzYoz5oqb8w01v6lE7yPGV3fM8MOqfDDT8Kq"

    # See documentation on defining a message payload.
    # Create a list containing up to 500 registration tokens.
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = [
        A1
    ]

    message = messaging.Message(
    notification=messaging.Notification(
        title='안녕하세요 타이틀 입니다',
        body='안녕하세요 메세지 입니다',
    ),
    token=A1,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

    return jsonify(rt="망했다")