from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings
from User.models import ClientRegister_Model, attack_prediction

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import os


# =========================
# HOME
# =========================
def index(request):
    return render(request, 'RUser/index.html')


# =========================
# LOGIN
# =========================
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = ClientRegister_Model.objects.get(username=username)

            if check_password(password, user.password):
                request.session['userid'] = user.id
                return redirect('ViewYourProfile')
            else:
                return render(request, 'RUser/login.html', {'error': 'Invalid password'})

        except ClientRegister_Model.DoesNotExist:
            return render(request, 'RUser/login.html', {'error': 'User not found'})

    return render(request, 'RUser/login.html')


# =========================
# REGISTER
# =========================
def Register1(request):
    if request.method == "POST":
        ClientRegister_Model.objects.create(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=make_password(request.POST.get('password')),
            phoneno=request.POST.get('phoneno'),
            country=request.POST.get('country'),
            state=request.POST.get('state'),
            city=request.POST.get('city'),
            address=request.POST.get('address'),
            gender=request.POST.get('gender')
        )

        return render(request, 'RUser/Register1.html', {'object': 'Registered Successfully'})

    return render(request, 'RUser/Register1.html')


# =========================
# PROFILE
# =========================
def ViewYourProfile(request):
    userid = request.session.get('userid')

    if not userid:
        return redirect('login')

    user = ClientRegister_Model.objects.get(id=userid)
    return render(request, 'RUser/ViewYourProfile.html', {'object': user})


# =========================
# ML PREDICTION
# =========================
def Predict_Web_Spoofing_Attack_Type(request):
    if request.method == "POST":
        url = request.POST.get('url')

        # ✅ Correct dataset path (IMPORTANT)
        dataset_path = os.path.join(settings.BASE_DIR, 'User', 'Datasets.csv')

        # ✅ Safety check
        if not os.path.exists(dataset_path):
            return render(request, 'RUser/Predict_Web_Spoofing_Attack_Type.html', {
                'objs': 'Dataset file not found'
            })

        df = pd.read_csv(dataset_path)

        df['Label'] = df['Label'].apply(lambda x: 0 if x == 0 else 1)

        cv = CountVectorizer()
        X = cv.fit_transform(df['URL'])
        y = df['Label']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = MultinomialNB()
        model.fit(X_train, y_train)

        vector = cv.transform([url])
        prediction = model.predict(vector)[0]

        if prediction == 0:
            result = 'No Phishing Attack'
        else:
            result = 'Phishing Attack Detected'

        # ✅ Save to database
        attack_prediction.objects.create(url=url, prediction=result)

        return render(request, 'RUser/Predict_Web_Spoofing_Attack_Type.html', {'objs': result})

    return render(request, 'RUser/Predict_Web_Spoofing_Attack_Type.html')