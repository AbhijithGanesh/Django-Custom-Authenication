from enum import unique
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from projectmanager.models import Employee


def ObjectChecker(obj):
    queryset = Employee.objects.values('EmployeeID')
    for i in list(queryset.values()):
        if obj in i['EmployeeID']:
            return True


def EmailFetcher(obj):
    queryset = Employee.objects.values_list('EmployeeID', 'EMail')
    for i in queryset:
        if obj == i[0]:
            return i[1]


class RegisterSerializer(serializers.ModelSerializer):
    employeeID = serializers.CharField(
        required = True, validators=[UniqueValidator])
    E_Mail = serializers.EmailField(
        required = True, validators=[UniqueValidator])
    username = serializers.CharField(
        required = True, validators=[UniqueValidator])
    password = serializers.CharField(
        write_only = True, required = True, validators = [validate_password]
    )
    Repeat_password = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = User
        fields = (
            "employeeID",
            "E_Mail",
            "username",
            "password",
            "Repeat_password",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["Repeat_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        elif not ObjectChecker(attrs["employeeID"]):
            raise serializers.ValidationError({
                "EmployeeID": "Enter a Valid Employee ID"
            })
        elif (EmailFetcher(attrs["employeeID"]) != attrs['E_Mail']):
            raise serializers.ValidationError({
                "E-Mail mistmatch": "The Enterred Email ID and your Employee Code mismatches!"
            })
        for i in User.objects.values_list('email'):
            if attrs['E_Mail'] == i[0]:
                raise serializers.ValidationError({
                    "E-Mail Error": "The Enterred Email ID is already registered"
                })

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data["username"],
            email = EmailFetcher(validated_data['employeeID'])
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
