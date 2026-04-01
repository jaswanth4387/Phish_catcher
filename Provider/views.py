from django.shortcuts import render, redirect
from django.db.models import Avg
from django.http import HttpResponse
import xlwt
import os

from User.models import ClientRegister_Model, attack_prediction, detection_ratio, detection_accuracy


# =========================
# DASHBOARD
# =========================
def dashboard(request):
    total_users = ClientRegister_Model.objects.count()
    total_predictions = attack_prediction.objects.count()
    safe_count = attack_prediction.objects.filter(prediction='No Phishing Attack').count()
    attack_count = attack_prediction.objects.filter(prediction='Phishing Attack Detected').count()

    return render(request, 'SProvider/dashboard.html', {
        'total_users': total_users,
        'total_predictions': total_predictions,
        'safe_count': safe_count,
        'attack_count': attack_count,
    })


# =========================
# LOGIN
# =========================
def serviceproviderlogin(request):
    if request.method == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')

        if admin == "Admin" and password == "Admin":
            detection_accuracy.objects.all().delete()
            return redirect('provider:View_Remote_Users')

    return render(request, 'SProvider/serviceproviderlogin.html')


# =========================
# VIEW USERS
# =========================
def View_Remote_Users(request):
    obj = ClientRegister_Model.objects.all()
    return render(request, 'SProvider/View_Remote_Users.html', {'objects': obj})


# =========================
# VIEW PREDICTIONS
# =========================
def View_Prediction_Of_Web_Spoofing_Attack_Status(request):
    obj = attack_prediction.objects.all()
    return render(request, 'SProvider/View_Prediction_Of_Web_Spoofing_Attack_Status.html', {'list_objects': obj})


# =========================
# RATIO CALCULATION
# =========================
def View_Web_Spoofing_Attack_Status_Ratio(request):
    detection_ratio.objects.all().delete()

    total = attack_prediction.objects.count()

    if total == 0:
        return render(request, 'SProvider/View_Web_Spoofing_Attack_Status_Ratio.html', {'objs': []})

    # Safe
    no_attack = attack_prediction.objects.filter(prediction='No Phishing Attack').count()
    ratio1 = (no_attack / total) * 100
    detection_ratio.objects.create(name='No Attack', ratio=ratio1)

    # Attack
    attack = attack_prediction.objects.filter(prediction='Phishing Attack Detected').count()
    ratio2 = (attack / total) * 100
    detection_ratio.objects.create(name='Attack', ratio=ratio2)

    obj = detection_ratio.objects.all()
    return render(request, 'SProvider/View_Web_Spoofing_Attack_Status_Ratio.html', {'objs': obj})


# =========================
# CHARTS
# =========================
def charts(request, chart_type):
    chart1 = detection_ratio.objects.values('name').annotate(dcount=Avg('ratio'))
    return render(request, "SProvider/charts.html", {'form': chart1, 'chart_type': chart_type})


def charts1(request, chart_type):
    chart1 = detection_accuracy.objects.values('name').annotate(dcount=Avg('ratio'))
    return render(request, "SProvider/charts1.html", {'form': chart1, 'chart_type': chart_type})


def likeschart(request, like_chart):
    charts = detection_accuracy.objects.values('name').annotate(dcount=Avg('ratio'))
    return render(request, "SProvider/likeschart.html", {'form': charts, 'like_chart': like_chart})


# =========================
# DOWNLOAD EXCEL
# =========================
def Download_Trained_DataSets(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Predicted_Datasets.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("sheet1")

    obj = attack_prediction.objects.all()

    row_num = 0
    for data in obj:
        row_num += 1
        ws.write(row_num, 0, data.url)
        ws.write(row_num, 1, data.prediction)

    wb.save(response)
    return response


# =========================
# TRAIN MODEL (FIXED 🔥)
# =========================
def train_model(request):
    try:
        import pandas as pd
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.model_selection import train_test_split
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn import svm
        from sklearn.metrics import accuracy_score

        detection_accuracy.objects.all().delete()

        # ✅ Safe path
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dataset_path = os.path.join(BASE_DIR, 'provider', 'Datasets.csv')

        print("Dataset Path:", dataset_path)

        df = pd.read_csv(dataset_path)

        # ✅ Fix column issues
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.upper()

        print("Columns:", df.columns)

        X_data = df['URL']
        y_data = df['LABEL']

        y_data = y_data.apply(lambda x: 0 if x == 0 else 1)

        cv = CountVectorizer()
        X = cv.fit_transform(X_data)
        y = y_data

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # Naive Bayes
        NB = MultinomialNB()
        NB.fit(X_train, y_train)
        acc = accuracy_score(y_test, NB.predict(X_test)) * 100
        detection_accuracy.objects.create(name="Naive Bayes", ratio=acc)

        # SVM
        model = svm.LinearSVC()
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test)) * 100
        detection_accuracy.objects.create(name="SVM", ratio=acc)

        # Logistic Regression
        reg = LogisticRegression(max_iter=1000)
        reg.fit(X_train, y_train)
        acc = accuracy_score(y_test, reg.predict(X_test)) * 100
        detection_accuracy.objects.create(name="Logistic Regression", ratio=acc)

        # Decision Tree
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        acc = accuracy_score(y_test, dtc.predict(X_test)) * 100
        detection_accuracy.objects.create(name="Decision Tree", ratio=acc)

        obj = detection_accuracy.objects.all()
        return render(request, 'SProvider/train_model.html', {'objs': obj})

    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})