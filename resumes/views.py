from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from .models import Resume
from .serializers import ResumeSerializer
from .permissions import ResumePermission

class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [ResumePermission]

    def get_queryset(self):
        user_perms = self.request.user.role.permissions.values_list('codename', flat=True)
        if "view_all_resumes" in user_perms:
            return Resume.objects.all()
        else:
            return Resume.objects.filter(user=self.request.user)

    def get_object(self):
        obj = get_object_or_404(Resume.objects.all(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
