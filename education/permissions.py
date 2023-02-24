from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    message = 'Вы не являетесь модератором'

    def has_permission(self, request, view):
        if request.user.has_perms(['education.view_course', 'education.change_course',
                                   'education.view_lesson', 'education.change_lesson']):
            return True


class IsManager(permissions.BasePermission):
    message = 'Вы не являетесь менеджером'

    def has_permission(self, request, view):
        if request.user.has_perms(['education.view_course', 'education.change_course',
                                   'education.add_course', 'education.delete_course',
                                   'education.add_lesson', 'education.delete_lesson',
                                   'education.view_lesson', 'education.change_lesson']):
            return True
        return False
