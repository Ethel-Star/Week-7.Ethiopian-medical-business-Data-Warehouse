import torch
import cv2
import os
import logging

# Load YOLOv5 pre-trained model (small version)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # You can change to yolov5m or yolov5l for better accuracy

# Folder paths
data_folder = "data/images"  # Input folder with images
output_folder = "data/detection_results"  # Output folder for detection results

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Set up logging
log_folder = 'log-yolo'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file = os.path.join(log_folder, 'detection.log')
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler(log_file, mode='w')
                    ])
logger = logging.getLogger(__name__)

# Function to process each image
for image_file in os.listdir(data_folder):
    if image_file.endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(data_folder, image_file)
        img = cv2.imread(img_path)

        # Perform inference on the image
        results = model(img)  # Run detection

        # Render results and save the output image with bounding boxes
        result_img = results.render()[0]  # Get the image with drawn bounding boxes

        # Save the result image
        cv2.imwrite(os.path.join(output_folder, f"detected_{image_file}"), result_img)

        # Log detection details (bounding boxes, classes, and scores)
        detection_details = []
        # Access the results in a way that's compatible with the latest YOLOv5
        for i, (box, conf, cls) in enumerate(zip(results.xywh[0], results.pred[0][:, 4], results.pred[0][:, 5])):
            class_name = model.names[int(cls)]  # Get the class name from YOLOv5's names attribute
            detection_details.append(f"Class: {class_name}, Confidence: {conf:.2f}, Box: {box.tolist()}")  # Convert box to list for better readability

        logger.info(f"Detections for {image_file}: {detection_details}")

        # Optionally, print detection details to the console
        print(f"Detections for {image_file}: {detection_details}")

# Log completion of the detection process
logger.info("Detection process completed for all images.")
