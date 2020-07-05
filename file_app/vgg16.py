
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
from keras import backend as K
import cv2
import os

img_width, img_height = 224, 224
top_model_weights_path = 'file_app/bottleneck_fc_model.h5'

def predict(image_path):
    K.clear_session()
    #tf.keras.backend.clear_session()    
    # load the class_indices saved in the earlier step
    print(image_path)
    image_path = os.getcwd()+image_path
    print(image_path)
    class_dictionary = np.load('file_app/class_indices.npy',allow_pickle=True).item()
    print('-1')
    num_classes = len(class_dictionary)

    # add the path to your test image below
    
    #image_path = 'test500.jpg' 
    orig = cv2.imread(image_path)
    print('-2')
    print("[INFO] loading and preprocessing image...")
    image = load_img(image_path, target_size=(224, 224))
    print('-3')
    image = img_to_array(image)
    print('-4')
    # important! otherwise the predictions will be '0'
    image = image / 255
    print('-5')
    image = np.expand_dims(image, axis=0)
    print('-6')
    # build the VGG16 network
    model = applications.VGG16(include_top=False,weights='imagenet')


    print("1")
    # get the bottleneck prediction from the pre-trained VGG16 model
    bottleneck_prediction = model.predict(image)
    
    # build top model
    model = Sequential()
    model.add(Flatten(input_shape=bottleneck_prediction.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='sigmoid'))

    print("2")
    model.load_weights(top_model_weights_path)
    print("3")
    # use the bottleneck prediction on the top model to get the final
    # classification
    class_predicted = model.predict_classes(bottleneck_prediction)

    probabilities = model.predict_proba(bottleneck_prediction)

    inID = class_predicted[0]

    inv_map = {v: k for k, v in class_dictionary.items()}

    label = inv_map[inID]

    #tf.keras.backend.clear_session()
    print(label)
    return label
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    K.clear_session()

# In[4]:
'''

orig = predict('./testing/500libcrop3')
plt.imshow(cv2.cvtColor(orig,cv2.COLOR_BGR2RGB), cmap = 'gray', interpolation = 'nearest')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()

'''
