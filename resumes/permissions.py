from rest_framework.permissions import BasePermission, SAFE_METHODS


class ResumePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False

        role_perms = user.role.permissions.values_list('codename', flat=True)
        if obj.user == user:
            return True

        if request.method in SAFE_METHODS:
            return 'view_all_resumes' in role_perms
        else:
            return 'edit_all_resumes' in role_perms
