# Adversarial Attacks on Image Captchas

To perform adversarial attacks on Image captchas to prevent bots from automating captcha tests using techniques like FGSM.

## Group Member

```

  Adhithya S            3
  Janaki Keerthi        26
  Jayasoorya Jithendra  28
  Jessal V A            29

```

## Project Guide:
```

    Prof. Rajasree R

```
## Project Co-ordinator:
```
  
    Prof. Vipin Vasu A.V.

```
## Tensorflowjs Implementation
```
  
    cd tensorflowCaptcha/local
    npm install
    node server.js

```
## Random Captcha Implementation

When client request for a captcha image, the server provide one by generating a random captcha image. For prediction, the image is sent back to the server, and the server reply with the predicted captcha. 

```
  cd RandomCaptchaModel
  FLASK_APP=predict_app.py flask run
```
Navigate to [http://127.0.0.1:5000/static/predict.html](http://127.0.0.1:5000/static/predict.html)
