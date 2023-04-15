from newspaper.models import Category, Tag, Post
from django.db.models import F, Sum,Case,When


def navigation(request):
    categories = Category.objects.all()
    top_categories = (
        Post.objects.values("category__pk", "category__name")
        .annotate(
            pk=F("category__pk"), name=F("category__name"), max_views=Sum("views_count")
        )
        .order_by("-views_count")
        .values("pk", "name", "max_views")
    )
    categories_ids =[top_category["pk"]for top_category in top_categories]
    order_by_max_views = Case(
        *[
            When(id= category["pk"],then=category["max_views"])
            for category in top_categories
        ]
    )
    top_categories =Category.objects.filter(pk__in=categories_ids).order_by(
        -order_by_max_views
    )
    print(top_categories)
    tags = Tag.objects.all()[:10]
    return {
        "categories": categories,
        "top_categories": top_categories,
        "tags": tags,
    }
