import boto3
import csv

with open('credentials.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]

photo = "lolololol.jpg"
client = boto3.client('rekognition', region_name='us-west-2', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
with open(photo, 'rb') as source_image:
    source_bytes = source_image.read()

response = client.detect_moderation_labels(
    Image={
        'Bytes': source_bytes
    },
    MinConfidence=70,
)


responses = response['ModerationLabels']

for item in responses:
    if "violence" in item['Name'].lower():
        print('********************* V I O L E N C E *********************')
        break

