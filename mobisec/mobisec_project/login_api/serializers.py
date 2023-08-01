from rest_framework import serializers
from app.models import Users
from django.contrib.auth.hashers import	make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'email', 'name', 'contact_no', 'password']

    def validate(self,data):
        password = data['password'].strip()
        if len(password) < 6:
            raise serializers.ValidationError('password length should be more than 6 digit')
        if len(password) > 10:
            raise serializers.ValidationError('password length should not be more than 6 digit')
        contact_no = data.get('contact_no',None)
        if not contact_no:
            raise serializers.ValidationError('contact no is mandatory')
        if len(str(contact_no)) < 6:
            raise serializers.ValidationError('contact no length should be more than 6 digit')
        if len(str(contact_no)) > 10:
            raise serializers.ValidationError('contact no length should not be more than 6 digit')
        name = data.get('name',None)
        if not name:
            raise serializers.ValidationError('name is mandatory')
        return data
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return Users.objects.create(**validated_data)
	
    def update(self, validated_data, instance):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        new_pass = make_password(validated_data.get('password'))
        instance.password = new_pass if new_pass else instance.password
        instance.save()