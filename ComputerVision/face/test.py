import cv2
import os
import tensorflow as tf

os.environ["CUDA_VISIBLE_DEVICES"]="0"
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)


cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if frame is None:
        print("EEEEEEEEEEEE")
    cv2.imshow("FRAME" ,frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()