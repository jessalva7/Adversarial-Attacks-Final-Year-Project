import base64
import tensorflow as tf
import numpy as np
from pathlib import Path
from PIL import Image
import io
import string
from io import BytesIO
import random
from skimage.io import imsave
import os
import matplotlib.pyplot as plt
from flask import request,render_template, send_file
from flask import jsonify
from flask import Flask

app = Flask(__name__)

char_choices = [lwchr for lwchr in string.ascii_lowercase]
testImage_dir = os.listdir( './static/test/' )
advImage_dir = os.listdir( './static/adversarial_images/' )

global numpy_captcha

def create_model():
    n_classes = 26
    kernel_initializer = tf.keras.initializers.glorot_uniform(seed=1337)
    trained_model = tf.keras.applications.xception.Xception(
        include_top=False,
        weights=None,
        input_shape=[100, 160, 3],
        pooling='max')

    c1 = tf.keras.layers.Dense(n_classes, activation='softmax', kernel_initializer = kernel_initializer)(trained_model.output)
    c2 = tf.keras.layers.Dense(n_classes, activation='softmax', kernel_initializer = kernel_initializer)(trained_model.output)
    c3 = tf.keras.layers.Dense(n_classes, activation='softmax', kernel_initializer = kernel_initializer)(trained_model.output)
    c4 = tf.keras.layers.Dense(n_classes, activation='softmax', kernel_initializer = kernel_initializer)(trained_model.output)
    c5 = tf.keras.layers.Dense(n_classes, activation='softmax', kernel_initializer = kernel_initializer)(trained_model.output)
    c6 = tf.keras.layers.Dense(n_classes, activation='softmax', kernel_initializer = kernel_initializer)(trained_model.output)

    return tf.keras.Model(inputs=trained_model.input, outputs=[c1, c2, c3, c4, c5, c6])
        
    

def preprocessImage(image):
    # if image.mode != "RGB":
    #     image = image.convert("RGB")
    image = tf.keras.preprocessing.image.img_to_array(image)
    
    image /= 255.
    image -= 0.5
    image *= 2.


    return image

print(' Loading Model... ')


model = create_model()
session = tf.Session(graph=tf.keras.backend.get_session().graph)
session.run(tf.global_variables_initializer())
model.load_weights('03_0.9974.h5')
model._make_predict_function()
print('Model Loaded')



@app.route('/predict', methods=['POST'])
def predict():
    
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))

    processedImage = preprocessImage(numpy_captcha)
    processedImage = processedImage[np.newaxis]
    
    with session.as_default():
        model.load_weights('03_0.9974.h5')
        predicted_prob = np.array(model.predict(processedImage))
    
    predicted_labels = np.argmax(predicted_prob[:,0,:],1)
    predicted_captcha = ''.join([chr(int(predicted_labels[i]) + ord('a')) for i in range(predicted_labels.shape[0])])

    response = {

            'prediction' : predicted_captcha

    }

    return jsonify(response)

@app.route('/',methods=['POST','GET'])
def captcha():
    noise = False
    if request.method == 'POST':
        message = request.get_json(force=True)
        noise = message['noise']

    captcha_text = random.choice(testImage_dir)
    if(noise == False):
        captcha_image = Image.open('./static/test/'+captcha_text)
    else:
        captcha_image = Image.open('./static/adversarial_images/'+captcha_text)
    
    global numpy_captcha
    numpy_captcha = np.array(captcha_image,dtype='float')
    buff = BytesIO()
    captcha_image.save(buff, format="png")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")

    print(captcha_text)
    response = {

        'image' : new_image_string
        
    }

    if request.method == 'POST':
        return jsonify(response)
    
    return render_template("predict.html", captcha_image = new_image_string)


    # captcha = Image.open(captcha)

    # captcha_image = np.array(captcha)

    # strIO = StringIO()
    # imsave(strIO, captcha_image, plugin='pil', format_str='png')
    # strIO.seek(0)
    #return send_file(captcha, mimetype='image/png',attachment_filename=captcha_text+'.png', as_attachment=True)
    
    # print(captcha_image.shape)
    # response = {

    #          'captcha' : captcha

    # }
