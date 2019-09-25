import boto3
import csv
import cv2
from PIL import Image
import io
import numpy as np

cap= cv2.VideoCapture(0)

clf= []
with open('accessKeys.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[0]
        secret_access_key = line[1]


client = boto3.client('rekognition', region_name='ap-south-1', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)


i = 0
text = "No disturbing content"

while(cap.isOpened()):
    i += 1
    ret, frame = cap.read()
    if ret == False:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.dstack([frame, frame, frame])
    pil_img = Image.fromarray(frame) # convert opencv frame (with type()==numpy) into PIL Image
    stream = io.BytesIO()
    pil_img.save(stream, format='JPEG') # convert PIL Image to Bytes
    bin_img = stream.getvalue()
 
    # Press Q on keyboard to  exit
    if cv2.waitKey(50) & 0xFF == ord('q'):
      break
    cv2.putText(frame, text, (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    if(i%40 == 0):
        text = "No disturbing content"
    if(i%5 == 0):
        response = client.detect_moderation_labels(
            Image={
                'Bytes': bin_img
            },
            MinConfidence=70,
        )
        responses = response['ModerationLabels']
        
        

        for item in responses:
            cv2.imwrite('videos/images/frame'+str(i)+' '+item['Name']+'.jpg',frame)
            print(item['Name'])
            text = item['Name']
            clf.append(item['Name'])
    cv2.imshow('Frame',frame)


cv2.destroyAllWindows()
