
from api.apitest.serializer import EmployeeSeriallizer
from django.http import HttpResponse
from apitest.models import Employees
from json import JSONEncoder
import json
from rest_framework.response import Response
from rest_framework.generics import (
CreateAPIView,
DestroyAPIView,
ListAPIView,
RetrieveAPIView,
UpdateAPIView,
RetrieveUpdateAPIView
)

class EmployeeListView(ListAPIView):
  

    serializer_class = EmployeeSeriallizer
    def get_queryset(self, *args, **kwargs):
        queryset = Employees.objects.all()
        # print(queryset)
        # queryset = json.dumps(queryset)
        return queryset

# class EmployeeListView(CreateAPIView):
#     """
#     List of all Strategy's
#     """
#     serializer_class = EmployeeSeriallizer
#     def create(self, *args, **kwargs):
#         queryset = Employees.objects.all()
#         # print(queryset)
#         # queryset = json.dumps(queryset)
#         return queryset
class EmployeeCreateView(CreateAPIView):
    serializer_class = EmployeeSeriallizer
    def perform_create(self, serializer):
        data = {}
        try:
            # name = self.request.data.get("deptname")
            # designation = self.request.data.get("designation")
            # companyname = self.request.data.get("companyname")
            # if RateCard.objects.filter(deptname=deptname, designation=designation, companyname=companyname).exists():
            #     data["status"] = "failed"
            #     data["message"] = MESSAGE.get("rate_card_exist")
            # else:
            employee= serializer.save()
            data['status'] = "success"
            data['message'] = 'created'
        except Exception as exception:
            data['status'] = "failed"
            data['message'] = 'something_wrong'
        return data
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.perform_create(serializer)
        if data['status'] == 'success':
            return Response(data=data, status=200)
        else:
            return Response(data=data, status=404)

class EmployeeEditView(RetrieveUpdateAPIView):
    queryset = Employees.objects.all()
    serializer_class =  EmployeeSeriallizer
    lookup_field = "name"
    def perform_update(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                rate = serializer.save()
                data['status'] = "success"
                data['message'] = 'update'
            else:
                data['message'] = 'failed'
                data['details'] = serializer.errors
                data['status'] = 'failed'
        except Exception as e:
            data['status'] = "failed"
            data['message'] = "failed"
        return data
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        data = self.perform_update(serializer)
        if data['status'] == 'success':
            return Response(data=data, status=200)
        else:
            return Response(data=data, status=404)
class EmployeeDeleteAPIView(DestroyAPIView):
    """
    Delete an 
    """
    queryset = Employees.objects.all()
    serializer_class =  EmployeeSeriallizer
    lookup_field = "name"
    def perform_destroy(self, instance):
        try:
            data = {}
            instance.delete()
            data['status'] = "success"
            data['message'] ="success"
            return data
        except Exception as exception:
            data['status'] = 'failed'
            data['message'] = 'failed'
            return data
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        if data['status'] == 'success':
            return Response(data=data, status=200)
        else:
            return Response(data=data, status=500)