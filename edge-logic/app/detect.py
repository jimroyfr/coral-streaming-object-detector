import cv2
from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils
from PIL import Image

#Constants
LABELS_PATH = "/models/labels.txt"
MODEL_PATH = "/models/model.tflite"

try:
    # Prepare labels.
    labels = dataset_utils.read_label_file(LABELS_PATH)
    print("Labels loaded")
except:
    print("Error loading labels")
    exit(1)

try:
    # Initialize engine.
    engine = DetectionEngine(MODEL_PATH)
except:
    print("Error loading model")
    exit(1)

def objects(frame):
    cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im)
    # Run inference.
    objs = engine.detect_with_image(pil_im,
                                  threshold=0.8,
                                  relative_coord=False,
                                  top_k=5)

    # Print and draw detected objects.
    for obj in objs:
        print('-----------------------------------------')
        if labels:
            label = labels[obj.label_id]
            print(label)
            print('score =', obj.score)
            box = obj.bounding_box.flatten().tolist()
            x0 = int(box[0])
            y0 = int(box[1])
            frame = cv2.rectangle(frame, (x0,y0), (int(box[2]),int(box[3])), (255,0,0), 2)
            frame = cv2.putText(frame, label, (x0, y0+30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
    
    return frame