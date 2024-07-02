def handler(event, context):
    print("Received event: " + str(event))
    for record in event['Records']:
        print("Message: " + record['body'])