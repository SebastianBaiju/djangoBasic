import logging
from django.conf import settings
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from apitest.models import Employees
logger = logging.getLogger(__name__)
class EmployeeSeriallizer(ModelSerializer):
    class Meta:
          model = Employees
          fields = ['name']