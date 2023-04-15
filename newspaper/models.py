from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 


class Category(TimeStampModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(TimeStampModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(TimeStampModel):
    STATUS_CHOICES = (
        ("published", "Published"),
        ("unpublished", "Un-published"),
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%Y/%m/%d", blank=False)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    published_at = models.DateTimeField(null=True, blank=True)
    views_count = models.PositiveBigIntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="unpublished"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    @property
    def latest_comments(self):
        comments = Comment.objects.filter(post=self).order_by("-created_at")
        return comments

class NewsLetter(TimeStampModel):
    email = models.EmailField()
    def __str__(self):
        return self.email


class Contact(TimeStampModel):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    name = models.CharField(max_length=50)
    email = models.EmailField()
    def __str__(self):
        return self.subject

class Comment(TimeStampModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    message = models.TextField()
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.messagae[:70]