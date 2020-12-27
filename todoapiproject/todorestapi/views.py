# views.py
from rest_framework import viewsets

from .serializers import UsersSerializer,TasksSerializer,TaskMappingSerializer
from .models import Users,Tasks,TaskMapping

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import generics


from django.contrib.auth import login

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, StudentsSerializer, UsersSerializer
from django.views.decorators.debug import sensitive_post_parameters

import psycopg2


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class UpdateUserData(APIView):
    def post(self, request):
        print(request.data)
        try:
            con = psycopg2.connect(database='todorest', user='postgres',
                        password='123456')
            with con:
                cur = con.cursor()
                cur.execute("insert into todorestapi_users(name,role) values(%s,%s)", (request.data['username'], request.data['role']))
                print(f"Number of rows updated: {cur.rowcount}")
                return Response({'status':'ok'})
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            return Response({'status':'error'})


# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('name')
    serializer_class = UsersSerializer

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.filter(role='Student').order_by('name')
    serializer_class = StudentsSerializer

class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer

class GetUsersList(APIView):
    def get(self, request):
        usernames = [user.name for user in Users.objects.all()]
        return Response(usernames)


class GetTeacherTasksList(generics.ListAPIView):
    serializer_class = TaskMappingSerializer
    def get_queryset(self):
        user = self.request.GET.get('createdby')
        print(user)
        # tasks = [task for task in Tasks.objects.all()]
        return TaskMapping.objects.filter(task__createdby__id=user)

class GetTasksMapViewSet(viewsets.ModelViewSet):
    queryset = TaskMapping.objects.all()
    serializer_class = TaskMappingSerializer

class GetStudentTasksList(generics.ListAPIView):
    serializer_class = TaskMappingSerializer
    def get_queryset(self):
        user = self.request.GET.get('username')
        print(user)
        # tasks = [task for task in Tasks.objects.all()]
        return TaskMapping.objects.filter(student__name=user)

class UsersByNameViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.filter(name='Naveen').order_by('name')
    serializer_class = UsersSerializer

class GetUsersByNameList(generics.ListAPIView):
    serializer_class = UsersSerializer
    def get_queryset(self):
        user = self.request.GET.get('username')
        print(user)
        return Users.objects.filter(name=user)


class UpdateTaskStatus(APIView):
    def post(self, request):
        print(request.data)
        try:
            con = psycopg2.connect(database='todorest', user='postgres',
                        password='123456')
            with con:
                cur = con.cursor()
                cur.execute("UPDATE todorestapi_taskmapping SET task_id=%s , student_id=%s , status=%s WHERE id=%s", (request.data['taskid'], request.data['createdby'], request.data['status'], request.data['id']))
                print(f"Number of rows updated: {cur.rowcount}")
                return Response({'status':'ok'})
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))
            return Response({'status':'error'})


class SaveTaskList(APIView):
    def post(self, request):
        print(request.data)
        try:
            con = psycopg2.connect(database='todorest', user='postgres',
                        password='123456')
            with con:
                cur = con.cursor()
                cur.execute("Insert into todorestapi_tasks(name,description,createdby_id,status_id) values(%s,%s,%s,%s) RETURNING id", (request.data['name'], request.data['description'], request.data['createdby'],1))
                print(f"Number of rows updated: {cur.rowcount}")
                last_row_id = cur.fetchone()[0]

                res = [('Created',last_row_id,val) for val in request.data['list']]
                # print the result
                print(res)

                query = "INSERT INTO todorestapi_taskmapping (status,task_id,student_id) VALUES (%s, %s, %s)"
                cur.executemany(query, res)
        except Exception as error:
            print ("Oops! An exception has occured:", error)
            print ("Exception TYPE:", type(error))

        # for x in request.data['list']:
        #     print(request.data['createdby'],request.data['name'],x)
        return Response({'scAS':'haschasbc'})
