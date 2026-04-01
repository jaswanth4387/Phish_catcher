from django.contrib import admin
from .models import ClientRegister_Model, attack_prediction, detection_accuracy, detection_ratio


admin.site.register(ClientRegister_Model)
admin.site.register(attack_prediction)
admin.site.register(detection_accuracy)
admin.site.register(detection_ratio)