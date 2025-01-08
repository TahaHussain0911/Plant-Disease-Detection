from flask import Flask, render_template, jsonify, request, Markup
from markupsafe import Markup
from model import predict_image
import utils
import cv2
import random
# import rtsp
import os
app = Flask(__name__)
# UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')

 
@app.route('/', methods=['GET'])
def home():
    try:
        # img = "C:/Users/DELL/Desktop/Disease Detection/test/test/PotatoEarlyBlight3.jpeg"
        img = os.path.join(app.root_path,'TestImages','PotatoEarlyBlight3.jpeg')

        prediction = predict_image(img)
        print(prediction,'prediction')
        res = Markup(utils.disease_dic[prediction])
        return render_template('display.html', status=200, result=res)
    except:
        pass

    
    # If captured image is corrupted, moving to else part
    return render_template('index.html')

@app.route('/new', methods=['GET', 'POST'])
def new():
    # path = "C:/Users/DELL/Desktop/Disease Detection/test/test/"
    path = os.path.join(app.root_path,'TestImages')

    if request.method == 'POST':
        cam_port = 0
        cam = cv2.VideoCapture(cam_port)
        if cam.isOpened():
            try:
            # while(True):
            # reading the input using the camera
                result, image = cam.read()
                
                # If image will detected without any error, 
                # show result
                
                # showing result, it take frame name and image 
                # output
                cv2.imshow("FYP-II", image)

                # saving image in local storage
                # Passing image path in first parameter of imwrite
                img_path = path + '/FYP24.jpg'
                cv2.imwrite(img_path, image)
                with open(img_path, "rb") as img_file:
                        img_binary = img_file.read()
                # If keyboard interrupt occurs, destroy image 
                # window
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                        # break
                prediction = predict_image(img_binary)
                print(prediction)
                res = Markup(utils.disease_dic[prediction])

                cv2.destroyAllWindows()
        
                # If captured image is corrupted, moving to else part
                return render_template('new.html', image_count=res)
            except Exception as e:
                print("Error occurred:", e)


    return render_template('new.html')
# import traceback

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            file = request.files['file']
            img = file.read()
            prediction = predict_image(img)
            print(prediction, 'prediction')
            res = Markup(utils.disease_dic[prediction])
            print(res, 'res')
            return jsonify(res)
            # return render_template('display.html', status=200, result=res)
        except Exception as e:
            print("Error occurred:", e)
            # traceback.print_exc()
            return render_template('index.html', status=500, res="Internal Server Error")
    return render_template('index.html', status=500, res="Internal Server Error")


if __name__ == "__main__":
    app.run(debug=True)
