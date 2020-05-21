"""canvasAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token
)

from django.conf.urls.static import static
from django.conf import settings

from establishments.views import EstablishmentViewSet
from courses.views import CourseViewSet
from enrollments.views import EnrollmentViewSet
from assignments.views import AssignmentViewSet
from groups.views import GroupViewSet
from professors.views import ProfessorViewSet
from students.views import StudentViewSet
from assistants.views import AssistantViewSet
from announcements.views import AnnouncementViewSet

router = routers.DefaultRouter()

router.register(r'establishments', EstablishmentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'professors', ProfessorViewSet)
router.register(r'students', StudentViewSet)
router.register(r'assistants', AssistantViewSet)
router.register(r'announcements', AnnouncementViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/token-auth/', obtain_jwt_token),
    url(r'^api/v1/token-refresh/', refresh_jwt_token),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)