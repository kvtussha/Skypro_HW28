from django.core.paginator import Paginator
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from ads.models import User, Location
from HW28 import settings

import json
from config import Config




class UserDataView(View):
    def get(self, request):
        with open(Config.USER_PATH_JSON, "r", encoding="utf-8") as file:
            data = json.load(file)

            for item in data:
                users = User(
                    first_name=item.get("first_name"),
                    last_name=item.get("last_name"),
                    username=item.get("username"),
                    password=item.get("password"),
                    role=item.get("role"),
                    age=item.get("age")
                )
                users.save()

        return JsonResponse({"message": "Success"}, status=200)

class UserListView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.annotate(total_ads=Count('ad'))

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "total_ads": user.total_ads,
                "locations": list(map(str, user.locations.all()))
            })

        response = {
            "items": users,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }

        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "age": user.age,
            "locations": list(map(str, user.locations.all()))
    })



@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "locations"]

    def post(self, request, *args, **kwargs):
        users_data = json.loads(request.body)

        users = User.objects.create(
            first_name=users_data["first_name"],
            last_name=users_data["last_name"],
            username=users_data["username"],
            password=users_data["password"],
            role=users_data["role"],
            age=users_data["age"],
        )

        for location_data in users_data.get("locations"):
            location, created = Location.objects.get_or_create(name=location_data)
            users.locations.add(location)
        users.save()

        try:
            users.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        return JsonResponse({
            "id": users.id,
            "first_name": users.first_name,
            "last_name": users.last_name,
            "username": users.username,
            "password": users.password,
            "role": users.role,
            "age": users.age,
            "locations": list(map(str, users.locations.all()))
        })



@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User

    def update(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        user_data = json.loads(request.body)

        if (item := user_data.get("first_name")):
            self.object.first_name = item
        if (item := user_data.get("last_name")):
            self.object.last_name = item
        if (item := user_data.get("username")):
            self.object.username = item
        if (item := user_data.get("password")):
            self.object.password = item
        if (item := user_data.get("role")):
            self.object.role = item
        if (item := user_data.get("age")):
            self.object.age = item

        for location_data in user_data.get("locations"):
            location, created = Location.objects.update_or_create(name=location_data)
            self.object.locations.add(location)

        self.object.save()

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "password": self.object.password,
            "role": self.object.role,
            "age": self.object.age,
            "locations": list(map(str, self.object.locations.all()))
        })



@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
