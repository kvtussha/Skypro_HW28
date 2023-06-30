from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from ads.models import Ad, Category, User
from HW28 import settings

import json
from config import Config


class AdDataView(View):
    """Добавить данные из json-файла в базу данных"""

    def get(self, request):
        with open(Config.AD_PATH_JSON, "r", encoding="utf-8") as file:
            data = json.load(file)

            for item in data:
                is_published = item.get("is_published").title()

                ads = Ad(
                    name=item.get("name"),
                    author_id=item.get("author_id"),
                    price=item.get("price"),
                    description=item.get("description"),
                    is_published=is_published,
                    image=item.get("image"),
                    category_id=item.get("category_id"),
                )
                ads.save()

        return JsonResponse({"message": "Success"}, status=200)


class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related("author").order_by("-price")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ads = []

        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author.first_name,
                "author_id": ad.author_id,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": ad.image.url if ad.image else None,
                "category": ad.category.name,
                "category_id": ad.category_id
            })

        response = {
            "items": ads,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count
        }

        return JsonResponse(response, safe=False)



class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.first_name,
            "author_id": ad.author_id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": ad.image.url if ad.image else None,
            "category": ad.category.name,
            "category_id": ad.category_id
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author_id", "price", "description", "is_published", "image", "category_id"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, pk=ad_data.get("author"))
        category = get_object_or_404(Category, pk=ad_data.get("category"))

        ad = Ad.objects.create(
            name=ad_data["name"],
            author=author,
            price=ad_data["price"],
            description=ad_data["description"],
            address=ad_data["address"],
            is_published=ad_data["is_published"],
            category=category
        )

        try:
            ad.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.first_name,
            "author_id": ad.author_id,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": ad.image.url if ad.image else None,
            "category": ad.category.name,
            "category_id": ad.category_id
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "image"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        if (item := ad_data.get("name")) is not None:
            self.object.name = item
        if (item := ad_data.get("price")) is not None:
            self.object.price = item
        if (item := ad_data.get("description")) is not None:
            self.object.description = item
        if (item := ad_data.get("is_published")) is not None:
            self.object.is_published = item

        self.object.author = get_object_or_404(User, pk=ad_data.get("author"))
        self.object.category = get_object_or_404(Category, pk=ad_data.get("category"))

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.first_name,
            "author_id": self.object.author_id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category": self.object.category.name,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ad
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.first_name,
            "author_id": self.object.author_id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category": self.object.category.name,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
