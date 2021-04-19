from wtforms import Form,StringField,PasswordField,validators,SubmitField
from flask import Flask,render_template,request
import pickle
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("main.html")


@app.route("/tahmin", methods =['POST','GET'])
def users():
    try:
        if request.method == 'POST':
            havadurumu = request.form.get('havad')
            sicaklik = request.form.get('sicak')
            nem = request.form.get('nem')
            ruzgar = request.form.get('ruzgar')
            
            bilgi = [havadurumu, sicaklik, nem, ruzgar]

            bilgiler = {"overcast":[0],
                    "rainy":[0],
                    "sunny":[0],
                    "temperature":[int(sicaklik)],
                    "nem":[int(nem)],
                    "ruzgar":[int(ruzgar)]}#var ise 0 yok ise 1

            if str(havadurumu).lower() == "kapalı":
                bilgiler["overcast"] = 1
            elif str(havadurumu).lower() == "yağmurlu":
               bilgiler["overcast"] = 1
            elif str(havadurumu).lower() == "güneşli":
                bilgiler["sunny"] = 1

            veri = pd.DataFrame.from_dict(bilgiler)
           

            model = pickle.load(open("model.kayit","rb"))
            global tahmin
            tahmin = model.predict(veri)
            
            if tahmin[0][0] > 0.7:
                image = "static/images/tenis.jpg" 
                return render_template("tahmin.html",resim = image)
                
            else:
                image = "static/images/uzgun.jpg"  
                return render_template("tahmin.html",resim=image)
                

            #mustafa = [kapali,gunesli,yagmurlu,sicak,nemm,ruzzgar]
            
    
    except:
        return render_template("tahmin.html", hata="hata oluştu")




if __name__ =="__main__":
    app.run(debug=True,port=1247)