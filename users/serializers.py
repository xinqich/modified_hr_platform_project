from rest_framework import serializers
from django.contrib.auth.models import Permission
from .models import User, Role

class UserSerializer(serializers.ModelSerializer):
    CANDIDATE = 'candidate'
    HR = 'hr'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (CANDIDATE, "Candidate"),
        (HR, 'HR manager'),
        (ADMIN, 'Administrator')
    ]

    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "password", 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        role, created = Role.objects.get_or_create(name=validated_data['role'])

        if created:
            role.description = "Candidates can view and edit their resumes"
            role.save()
            add_resume = Permission.objects.get(codename="add_resume")
            change_resume = Permission.objects.get(codename="change_resume")
            view_resume = Permission.objects.get(codename="view_resume")
            delete_resume = Permission.objects.get(codename="delete_resume")
            view_all_resumes = Permission.objects.get(codename="view_all_resumes")
            edit_all_resumes = Permission.objects.get(codename="edit_all_resumes")

            role.permissions.set([add_resume, change_resume, view_resume, delete_resume])

            if role.name == self.HR:
                role.permissions.add(view_all_resumes)
            if role.name == self.ADMIN:
                role.permissions.add(view_all_resumes, edit_all_resumes)


        user.role = role
        user.save()

        return user