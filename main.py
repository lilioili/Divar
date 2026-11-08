import tkinter as tk
from tkinter import filedialog
import pandas as pd
from mlforkidsimages import MLforKidsImageProject
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
from PIL import Image,ImageTk

def upload():
    global prediction_i , img1
    path_image = filedialog.askopenfilename()
     
    img1 = ImageTk.PhotoImage(Image.open(path_image).resize((100,100)))
    L_image = tk.Label(screen,image=img1)
    L_image.place(x=100,y=500,anchor="center")

    prediction_i = model_i.prediction(path_image)    
    print(prediction_i)
    
def processing():
    age_years = E_age.get()
    brand = E_brand.get()   
    city = E_city.get()
    appearance = E_appearance.get()
    description = E_description.get()

    test=[[age_years,brand,city,appearance]]
    test=pd.DataFrame(test,columns=["age_years","brand","city","appearance"])

    appearance_map = {"درحدنو":3,"خوب":2,"متوسط":1,"ضعیف":0}

    test["appearance"]=test["appearance"].map(appearance_map)


    # -------------------------
    # مشخص کردن همه حالت‌های ممکن
    # -------------------------

    test["brand"] = pd.Categorical(
    test["brand"],
    categories=['تلویزیون آریا', 'تلویزیون سپهر', 'تلویزیون نوین', 'تلویزیون پارس',
        'دوچرخه آریا', 'دوچرخه سپهر', 'دوچرخه نوین', 'دوچرخه پارس',
        'لپ\u200cتاپ آریا', 'لپ\u200cتاپ سپهر', 'لپ\u200cتاپ نوین',
        'لپ\u200cتاپ پارس', 'مبل آریا', 'مبل سپهر', 'مبل نوین', 'مبل پارس',
        'یخچال آریا', 'یخچال سپهر', 'یخچال نوین', 'یخچال پارس']
    )

    test["city"] = pd.Categorical(
    test["city"],
    categories=['اصفهان', 'تهران', 'شیراز', 'مشهد', 'کرج']
    )

    

    test = pd.get_dummies(
        test,
        columns=[
            "brand","city"
        ],
        dtype=int
    )
    prediction_r = int(model_r.predict(test.values)[0])

    description_transformed = tfidf.transform([description])
    prediction_text = model_text.predict(description_transformed)[0]
    L_text = tk.Label(screen,text=f"{prediction_i['class_name']} شما {prediction_text}است \n قیمت حدودی {prediction_r} تومان است ± 5992404",bg="#101827",font=("comic sans ms",11),fg="#FFFFFF")
    L_text.place(x=450,y=200,height=50,anchor="center")
     

##############################################################################
key = "E:/ml_ilia/divar/datasets"

model_i = MLforKidsImageProject(key)
model_i.train_model()
#############################################################################
data_train = pd.read_csv("E:/ml_ilia/divar/train.csv")
data_test = pd.read_csv("E:/ml_ilia/divar/test.csv")

x_train_r = data_train[["age_years","appearance","brand","city"]]
y_train_r = data_train["price_toman"]

x_test_r = data_test[["age_years","appearance","brand","city"]]
y_test_r = data_test[["price_toman"]]

model_r = LinearRegression()

scaler = StandardScaler()

x_train_r = pd.get_dummies(x_train_r,columns=["brand","city"],dtype=int)
appearance_map = {"درحدنو":3,"خوب":2,"متوسط":1,"ضعیف":0}
x_train_r["appearance"]=x_train_r["appearance"].map(appearance_map)
x_train_r_scale = scaler.fit_transform(x_train_r)

model_r.fit(x_train_r_scale,y_train_r)

x_test_r = pd.get_dummies(x_test_r,columns=["brand","city"],dtype=int)
appearance_map = {"درحدنو":3,"خوب":2,"متوسط":1,"ضعیف":0}
x_test_r["appearance"]=x_test_r["appearance"].map(appearance_map)
x_test_r_scale = scaler.fit_transform(x_test_r)

predictions_r = model_r.predict(x_test_r_scale).reshape(-1,1)
data_test["predictions_r"]=predictions_r

MAE = np.mean(np.abs(y_test_r-predictions_r))
MSE = np.mean(np.square(predictions_r-y_test_r))
RMSE = np.sqrt(np.mean(np.square(predictions_r-y_test_r)))


####################################################################################
data_train_text=data_train["description"]
y_train_text = data_train["condition"]

model_text=LinearSVC()
tfidf = TfidfVectorizer()

data_train_text_transformed = tfidf.fit_transform(data_train_text)
model_text.fit(data_train_text_transformed,y_train_text)

###########################################################################################
screen = tk.Tk()

screen.geometry("900x700")
screen.title("دیوار")
screen.config(bg="#101827")
#######################################################################################
button_upload = tk.Button(screen,text="عکس انتخاب",bg="#FF7070",command=upload,font=("comic sans ms",17))
button_upload.place(x=100,y=600,width=100,height=40,anchor="center")

button_p = tk.Button(screen,text="اطلاعات پردازش",bg="#FF7070",command=processing,font=("comic sans ms",17))
button_p.place(x=500,y=600,width=150,height=40,anchor="center")
#############################################################################################
E_age = tk.Entry(screen)
E_age.place(x=800,y=350,anchor="center")

E_brand = tk.Entry(screen)
E_brand.place(x=800,y=290,anchor="center")

E_city = tk.Entry(screen)
E_city.place(x=800,y=410,anchor="center")

E_appearance = tk.Entry(screen)
E_appearance.place(x=800,y=470,anchor="center")

E_description = tk.Entry(screen)
E_description.place(x=400,y=350,width=250,height=25,anchor="center")
###############################################################################################
L_age = tk.Label(screen,text="age_year",bg="#101827",fg="#F8FAFC",font=("Arial", 11, "bold"))
L_age.place(x=800,y=330,anchor="center")
 
L_city = tk.Label(screen,text="city",bg="#101827",fg="#F8FAFC",font=("Arial", 11, "bold"))
L_city.place(x=800,y=390,anchor="center")

L_brand = tk.Label(screen,text="brand",bg="#101827",fg="#F8FAFC",font=("Arial", 11, "bold"))
L_brand.place(x=800,y=270,anchor="center")

L_appearance = tk.Label(screen,text="appearance",bg="#101827",fg="#F8FAFC",font=("Arial", 11, "bold"))
L_appearance.place(x=800,y=450,anchor="center")
















screen.mainloop()