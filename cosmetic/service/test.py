from flask import Blueprint
from flask.json import jsonify
from firebase_admin import messaging

SERVER_API_KEY = "AAAA82vbQso:APA91bGoMlx434BzWaxeF5xQmUKOnXOz7LpWfOCLXZ7vyWMYkFTQufkfKAleBbzFlYI92Ru1hLsvyKUNf49Akqkr0hPqvZs-asGze15DGOtQv3-S080rvXRDrTjev_FsUHCE0eaP63KG"
SENDER_ID = "1045486584522"
bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/real', methods=["GET"])
def test():
    A1 = "cydhF1U6RcOFNafwNqz7xJ:APA91bFnDCXl10JmqL2fsnFqNSpJvW4FYibaANWqF2J2Fk2idurz8cgnvxseiG2VBmtDnzpwI1XszQLwRkon6IsztvYBtyY3Dukc5SwjYzYoz5oqb8w01v6lE7yPGV3fM8MOqfDDT8Kq"

    # See documentation on defining a message payload.
    # Create a list containing up to 500 registration tokens.
    # These registration tokens come from the client FCM SDKs.
    registration_tokens = [
        A1
    ]

    message = messaging.MulticastMessage(
        data={'score': '850', 'time': '2:45'},
        tokens=registration_tokens,
    )
    print(message)
    response = messaging.send_multicast(message)
    print(response)
    if response.failure_count > 0:
        responses = response.responses
        failed_tokens = []
        for idx, resp in enumerate(responses):
            if not resp.success:
                # The order of responses corresponds to the order of the registration tokens.
                failed_tokens.append(registration_tokens[idx])
        print('List of tokens that caused failures: {0}'.format(failed_tokens))

    return jsonify(rt="망했다")