import cv2
import face_recognition
import pickle
import time
import os
import tensorflow as tf

os.environ["CUDA_VISIBLE_DEVICES"]="0"
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)


file_name = ('Olivia.mp4')
encoding_file = 'encodings.pickle'
Unknow_name = 'Unknown'

model_method = 'HOG'


def detectAndDisplay(image):
    start_time = time.time()
    image = cv2.resize(image, (256,256), interpolation= cv2.INTER_LINEAR)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, 
                                            model = model_method)
    encodings = face_recognition.face_encodings(rgb, boxes)
    
    names = []
    
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"] ,
                                                 encoding)
        name = Unknow_name
        
        if True in matches:
            
            matchesIdxs = [i for (i,b) in enumerate(matches) if b]
            counts = {}
            
            for i in matchesIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name,0) +1
                
                
            name = max(counts, key = counts.get)
        names.append(name)
        
    for ((top, right, bottom, left), name) in zip(boxes, names):
        
        y = top -15 if top -15 >15 else top+15
        color = (0,255,0)
        line = 2
        if(name == Unknow_name):
            color = (0,0,255)
            line = 1
            name = ''
        
        cv2.rectangle(image, (left, top), (right, bottom), color, line)
        y = top -15 if top -15 >15 else top+15
        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.75, color, line)
        
    
    end_time = time.time()
    print(end_time- start_time)
    image = cv2.resize(image, None, fx= 2, fy=2)
    cv2.imshow("FACE", image)  



data = pickle.loads(open(encoding_file, "rb").read())
cap = cv2.VideoCapture(0)

if not cap.isOpened:
    print('EEEEEE')
    exit(0)
    
while True:
    ret, frame = cap.read()
    if frame is None:
        print("EEEEEEEEEEEE")
    detectAndDisplay(frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()