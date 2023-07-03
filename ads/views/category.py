from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from ads.models import Category

import json
from config import Config

class CategoryDataView(View):
    def get(self, request):
        with open(Config.CATEGORY_PATH_JSON, "r", encoding="utf-8") as file:
            data = json.load(file)


            for item in data:
                categories = Category(id=item.get("id"), name=item.get("name"))
                categories.save()

        return JsonResponse({"message": "Success"}, status=200)


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('name')
        categories = []
        for category in self.object_list:
            categories.append({
                "id": category.id,
                "name": category.name
            })

        return JsonResponse(categories, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({
            "id": cat.id,
            "name": cat.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        categories_data = json.loads(request.body)

        categories = Category.objects.create(
            name=categories_data["name"]
        )

        try:
            categories.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        return JsonResponse({
            "id": categories.id,
            "name": categories.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def put(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        cat_data = json.loads(request.body)
        if (item := cat_data.get("name")) is not None:
            self.object.name = item

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)