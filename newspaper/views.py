from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, View, TemplateView
from django.db.models import Q
from newspaper.models import Post, Category
from newspaper.forms import NewsLetterForm, ContactForm, CommentForm, PostForm
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    model = Post
    template_name = "aznews/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        status="published", published_at__isnull=False
    ).order_by("-published_at")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_post"] = (
            Post.objects.filter(status="published", published_at__isnull=False)
            .order_by("-views_count")  # descending order
            .first()
        )
        context["most_viewed_posts"] = Post.objects.filter(
            status="published", published_at__isnull=False
        ).order_by("-views_count")[:3]

        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            status="published",
            published_at__isnull=False,
            published_at__gte=one_week_ago,
        ).order_by("-views_count")[:7]

        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "aznews/detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        obj = self.get_object()
        obj.views_count += 1
        obj.save()


        obj = self.get_object()
        context["previous_post"] = (
            Post.objects.filter(
                id__lt=obj.id,
                status="published",
                published_at__isnull=False,
            )
            .order_by("-id")
            .first()
        )
        context["next_post"] = (
            Post.objects.filter(
                id__gt=obj.id,
                status="published",
                published_at__isnull=False,
            )
            .order_by("id")
            .first()
        )

        context["recent_posts"] = Post.objects.filter(
            status="published",
            published_at__isnull=False,
        ).order_by("-published_at")[:4]

        return context


class PostListView(ListView):
    model = Post
    template_name = "aznews/list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        status="published", published_at__isnull=False
    ).order_by("-published_at")
    paginate_by = 10


class PostSearchView(View):
    def get(self, request, *args, **kwargs):
        print(request.GET)
        query = request.GET["query"]
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(contain__icontains=query)
        )
        return render(
            request,
            "aznews/list.html",
            {"query": query, "posts": posts},
        )


class NewsLetterView(View):
    form_class = NewsLetterForm

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get("x-requested-with")
        print(is_ajax)
        if is_ajax == "XMLHttpRequest":
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                        "sucess": True,
                        "message": "Successfully submitted your email address.We will contact you soon",
                    },
                    status=200,
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Something went wrong.Please make sure your form is correct",
                    },
                    status=400,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process.Must be ajax request.",
                },
                status=400,
            )


class PostByCategory(ListView):
    model = Post
    template_name = "aznews/list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        super().get_queryset()
        queryset = Post.objects.filter(
            status="published",
            published_at__isnull=False,
            category=self.kwargs["cat_id"],
        )
        return queryset


class PostByTag(ListView):
    model = Post
    template_name = "aznews/list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        super().get_queryset()
        queryset = Post.objects.filter(
            status="published",
            published_at__isnull=False,
            tag=self.kwargs["tag_id"],
        )
        return queryset


class AboutUsView(TemplateView):
    template_name = "aznews/about.html"


class ContactView(View):
    template_name = "aznews/contact.html"
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Successfully submitted your messsage. We will contact you soon ",
            )
        else:
            messages.error(request, "Cannot submit your message.Something went wrong.")

        return render(request, self.template_name, {"form": form})


class CommentView(View):
    form_class = CommentForm
    template_name = "aznews/detail.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        post_id = request.POST["post"]

        if form.is_valid():
            form.save()
            return redirect("postdetail", post_id)
        else:
            post = Post.objects.get(id=post_id)
        return render(
            request,
            self.template_name,
            {"post": post, "form": form},
        )


class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "admin/post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_at__isnull=True).order_by("-published_at")


class PostPublishView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        post.published_at = timezone.now()
        post.save()
        return redirect("post-list")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "admin/post_create.html"
    success_url = reverse_lazy("draft-list")

    def form_valid(self, form):
        # make logged-in user as a author of the post
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("post-list")


class PostUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
        return render(
            request,
            "admin/post_create.html",
            {"form": form},
        )

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            form.save()
            return redirect("post-list")
