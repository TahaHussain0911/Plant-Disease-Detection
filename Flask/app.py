from flask import Flask, render_template, jsonify, request, Markup
from markupsafe import Markup
# from flask_mysqldb import MySQL
from model import predict_image
import utils
import cv2
import random
# import rtsp
import os
app = Flask(__name__)
# UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'flask'
 
# mysql = MySQL(app)

@app.route('/', methods=['GET'])
def home():
    path=os.path.join(app.root_path,'static','cam')
    # path = "/home/waqas/Documents/FYP II/Plant_AI-master/fyp-ii/Flask/static/cam"
    cam_port = 0
    a = 0
    cam = cv2.VideoCapture('rtsp://admin:Talha1234@192.168.100.48/H264?ch=1&subtype=0')
    # Define the codec and create VideoWriter object
    # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    # out = cv2.VideoWriter('/home/Documents/FYP II/Plant_AI-master/fyp-ii/Flask/static/cam/output.mp4', fourcc, 20.0, (640, 480))
    if cam.isOpened():
        while(True):
            # reading the input using the camera
            result, image = cam.read()
            
            # If image will detected without any error, 
            # show result
            # Converts to grayscale space, OCV reads colors as BGR
            # frame is converted to gray
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            cv2.rectangle(image,(900,450),(500,200),(0,255,0),6)

            # output the frame
            # out.write(gray)
            
            # showing result, it take frame name and image 
            # output
            cv2.imshow("FYP-II", image)

            cv2.imshow("Gray", gray)

            # saving image in local storage
            # Passing image path in first parameter of imwrite
            cv2.imwrite(path+"/FYP"+str(a)+".jpg", image)
            a = a + 1
            # If keyboard interrupt occurs, destroy image 
            # window
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cam.release()
    cv2.destroyAllWindows()

    try:
        # img = "C:/Users/DELL/Desktop/Disease Detection/test/test/PotatoEarlyBlight3.jpeg"
        img = os.path.join(app.root_path,'TestImages','PotatoEarlyBlight3.jpeg')

        prediction = predict_image(img)
        print(prediction,'prediction')
        res = Markup(utils.disease_dic[prediction])
        return render_template('display.html', status=200, result=res)
    except:
        pass
    
    test='abc'
    # cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO test(img) VALUES (%s)", [test])
    # mysql.connection.commit()
    # cur.close()
    
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

            return render_template('display.html', status=200, result=res)
        except Exception as e:
            print("Error occurred:", e)
            # traceback.print_exc()
            return render_template('index.html', status=500, res="Internal Server Error")
    return render_template('index.html', status=500, res="Internal Server Error")


if __name__ == "__main__":
    app.run(debug=True)
