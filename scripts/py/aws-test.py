import boto3
import sys, os

s2Arn = "arn:aws:s3:::edu.ucla.remap.fssi.ingest"
sqsArn = "arn:aws:sqs:us-west-1:756428767688:s3-touchdesigner"
snsArn = "arn:aws:s3:::edu.ucla.remap.fssi.ingest"

def updloadS3():
    s3 = boto3.client('s3')
    fname = sys.argv[0]
    key = os.path.basename(fname)
    s3.upload_file(fname, "edu.ucla.remap.fssi.ingest", key)
    print('uploaded {} as {}'.format(fname, key))
    # s3.download_file("edu.ucla.remap.fssi.ingest", "hello.txt", "/Users/jefft0/Desktop/hello2.txt")

def testDynamo():
    dynamodb = boto3.resource('dynamodb', region_name = "us-west-1")
    table = dynamodb.Table("edu.ucla.remap.fssi.image_meta")
    table.put_item(Item = { "image_name": "test-image.jpg", "meta": '{ "hash": "99999", "content-type": "image/jpeg" }' })
    response = table.get_item(Key={"image_name": "test-image.jpg"})
    print(response["Item"]["meta"])

def receiveSqs():
    sqs = boto3.resource('sqs')
    print('hey, here are all your queues:')
    for queue in sqs.queues.all():
        print(queue.url)
    queueName = 's3-touchdesigner'
    try:
        queue = sqs.get_queue_by_name(QueueName=queueName)
        while True:
            print("polling queue...")
            for message in queue.receive_messages():
                print('message: {0}'.format(message.body))
                message.delete()
    except Exception as e:
        print("error working with the queue", e)



updloadS3()
# testDynamo()
# receiveSqs()
