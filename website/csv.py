# import os
# import csv

# path = r'website/DataSet/numbers'
# array = [num for num in os.listdir(path)]


# with open('number.csv', 'w', newline='') as csvfile:
#     csv_writer = csv.writer(csvfile)
    
#     csv_writer.writerow(['Number', 'Links'])
    
#     for arr in array:
#         arr = str(arr)
#         video_path = os.path.join(path, arr)  
#         if os.path.isdir(video_path):
#             links = [video_path]
        
#             for link in links:
#                 csv_writer.writerow([arr, link]) 

# path = r'website/DataSet/operators/'
# array = [num for num in os.listdir(path)]


# with open('operator.csv', 'w', newline='') as csvfile:
#     csv_writer = csv.writer(csvfile)
    
#     csv_writer.writerow(['Operator', 'Links'])
    
#     for arr in array:
#         arr = str(arr)
#         video_path = os.path.join(path, arr)  
#         if os.path.isdir(video_path):
#             links = [video_path]
        
#             for link in links:
#                 csv_writer.writerow([arr, link]) 

# import cv2
# import numpy as np

# low_green = np.array([15,52,72])
# high_green = np.array([102,255,255])

# path = r"website\DataSet\test_data\test\test (40).jpg"
# image = cv2.imread(path)

# image = cv2.cvtColor(image , cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(image , low_green , high_green)
# canny = cv2.Canny(image , 90 , 255)


# while True:
#     cv2.imshow("Frame" , canny)

#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break
       
