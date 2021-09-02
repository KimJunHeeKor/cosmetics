from flask import Blueprint
from flask.json import jsonify
from firebase_admin import messaging

SERVER_API_KEY = "AAAA82vbQso:APA91bGoMlx434BzWaxeF5xQmUKOnXOz7LpWfOCLXZ7vyWMYkFTQufkfKAleBbzFlYI92Ru1hLsvyKUNf49Akqkr0hPqvZs-asGze15DGOtQv3-S080rvXRDrTjev_FsUHCE0eaP63KG"
SENDER_ID = "1045486584522"
bp = Blueprint('test', __name__, '/test')

@bp.route('/real', methods=["GET"])
def test():
    registration_token = "cydhF1U6RcOFNafwNqz7xJ:APA91bFnDCXl10JmqL2fsnFqNSpJvW4FYibaANWqF2J2Fk2idurz8cgnvxseiG2VBmtDnzpwI1XszQLwRkon6IsztvYBtyY3Dukc5SwjYzYoz5oqb8w01v6lE7yPGV3fM8MOqfDDT8Kq"

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'score': '850',
            'time': '2:45',
        },
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)