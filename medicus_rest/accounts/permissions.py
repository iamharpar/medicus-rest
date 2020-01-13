from rest_framework.permissions import BasePermission

# create your permissions here.


class IsOrganization(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'to_organization')


class IsMedicalStaff(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'to_medical_staff')


class IsVerifiedMedicalStaff(IsMedicalStaff):
    def has_permission(self, request, view):
        is_medical_staff = super().has_permission(request, view)
        if is_medical_staff:
            return request.user.to_medical_staff.is_verified
        return False
