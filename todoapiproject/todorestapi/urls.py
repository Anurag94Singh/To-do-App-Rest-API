from django.urls import include, path
from rest_framework import routers
from . import views

from knox import views as knox_views
from .views import LoginAPI, RegisterAPI, UserAPI
from django.urls import path

router = routers.DefaultRouter()
router.register(r'users', views.UsersViewSet)

router.register(r'userbyname', views.UsersByNameViewSet)

router.register(r'students', views.StudentsViewSet)

router.register(r'tasks', views.TasksViewSet)

router.register(r'taskmap', views.GetTasksMapViewSet)

# router.register(r'studenttasks', views.GetStudentTasksViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('GetUsersList/', views.GetUsersList.as_view()), #GetUsersByNameList
    path('GetUsersByName/', views.GetUsersByNameList.as_view()),
    path('SaveTaskList/', views.SaveTaskList.as_view()),
    path('UpdateUserData/', views.UpdateUserData.as_view()),
    path('UpdateTaskStatus/', views.UpdateTaskStatus.as_view()),
    path('GetTeacherTasksList/', views.GetTeacherTasksList.as_view()),
    path('GetStudentTasksList/', views.GetStudentTasksList.as_view()),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
