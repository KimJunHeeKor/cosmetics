# from firebase_admin import messaging

# import os
# import firebase_admin

# from firebase_admin import credentials

# cred_path = os.path.join("cosmetic/data/", "serviceAccountKey.json")
# cred = credentials.Certificate(cred_path)
# firebase_admin.initialize_app(cred)

# SERVER_API_KEY = "AAAA82vbQso:APA91bGoMlx434BzWaxeF5xQmUKOnXOz7LpWfOCLXZ7vyWMYkFTQufkfKAleBbzFlYI92Ru1hLsvyKUNf49Akqkr0hPqvZs-asGze15DGOtQv3-S080rvXRDrTjev_FsUHCE0eaP63KG"
# SENDER_ID = "1045486584522"


# reg_token = "cydhF1U6RcOFNafwNqz7xJ:APA91bFnDCXl10JmqL2fsnFqNSpJvW4FYibaANWqF2J2Fk2idurz8cgnvxseiG2VBmtDnzpwI1XszQLwRkon6IsztvYBtyY3Dukc5SwjYzYoz5oqb8w01v6lE7yPGV3fM8MOqfDDT8Kq"

# # See documentation on defining a message payload.
# # Create a list containing up to 500 registration tokens.
# # These registration tokens come from the client FCM SDKs.

# message = messaging.Message(
# notification=messaging.Notification(
#     title='안녕하세요 타이틀 입니다',
#     body='안녕하세요 메세지 입니다',
# ),
# token=reg_token,
# )

# response = messaging.send(message)
# # Response is a message ID string.
# print('Successfully sent message:', response)

from pyfcm import FCMNotification

#서버키
push_service = FCMNotification(api_key="AAAA82vbQso:APA91bGoMlx434BzWaxeF5xQmUKOnXOz7LpWfOCLXZ7vyWMYkFTQufkfKAleBbzFlYI92Ru1hLsvyKUNf49Akqkr0hPqvZs-asGze15DGOtQv3-S080rvXRDrTjev_FsUHCE0eaP63KG")

 
#이미지
extra_notification_kwargs = {'image': "2.jpg" }
    
#토큰
registration_id = "cydhF1U6RcOFNafwNqz7xJ:APA91bFnDCXl10JmqL2fsnFqNSpJvW4FYibaANWqF2J2Fk2idurz8cgnvxseiG2VBmtDnzpwI1XszQLwRkon6IsztvYBtyY3Dukc5SwjYzYoz5oqb8w01v6lE7yPGV3fM8MOqfDDT8Kq"

#메세지
message_title = "뚜니 문자왔어요."
message_body = "먀우."
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, extra_notification_kwargs=extra_notification_kwargs )
 
print (result)