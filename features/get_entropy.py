import numpy as np
import cv2
from skimage.feature import greycomatrix
import os
import statistics




frames_dir = "frames\\{}\\"

def get_entropy(videoId):
    b = []
    if os.path.exists(frames_dir.format(videoId)):
      for file in os.listdir(frames_dir.format(videoId)):
          if file.endswith(".bmp"):
              image_path = os.path.join(frames_dir.format(videoId), file)
              #print (image_path)
              img = cv2.imread(image_path)
              img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
              b.append(entropy(img))
    #print ("totale :")
    return statistics.mean(b)

    
def entropy(img):
   glcm = np.squeeze(greycomatrix(img, distances=[1], angles=[0], symmetric=True, normed=True))
   entropy = -np.sum(glcm*np.log2(glcm + (glcm==0))) 
   #print (entropy)
   return  entropy