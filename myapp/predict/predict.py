import cv2
import keras
from keras import backend as K
import numpy as np
from keras.models import load_model

def preprocess(path):
	img=cv2.imread(path)
	img=cv2.resize(img,(220,155))
	bw_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	bw_image = 255 - bw_image
	_ ,threshold_image = cv2.threshold(bw_image, 50, 255,cv2.THRESH_BINARY)
	threshold_image = threshold_image.astype('float32')
	threshold_image /=255
	return(threshold_image)
def contrastive_loss(y_true, y_pred):
    margin = 1
    square_pred = K.square(y_pred)
    margin_square = K.square(K.maximum(margin - y_pred, 0))
    return K.mean(y_true * square_pred + (1 - y_true) * margin_square)

def load(org_path,forg_path):
	model = load_model('/home/user/Documents/project/myproject/myapp/predict/entho3.model',custom_objects={'contrastive_loss':contrastive_loss})

	img1=preprocess(org_path)

	img2=preprocess(forg_path)			
	prediction = model.predict([[img1],[img2]])
	pred = prediction.ravel() < 0.5
	return (pred)
