from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=False)


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name


class ItemBase(models.Model):
    class Meta:
        abstract = True

    tour_name = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='tours/%Y/%m', default=None)
    created_date = models.DateTimeField(auto_now_add=True)  # auto_now_add: lấy thời gian hiện tại
    updated_date = models.DateTimeField(auto_now=True)  # auto_now: cập nhật mỗi lần thay đổi
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.tour_name


class Tour(ItemBase):
    class Meta:
        unique_together = ('tour_name', 'category')  # khong được trùng
        ordering = ["id"]

    description = models.TextField(null=True, blank=True)  # blank: rỗng
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True)  # on_delete=models.SET_NULL Khi cate xóa trường này sẽ rỗng


class TourDetail(ItemBase):  # chi tiet tour
    class Meta:
        unique_together = ('tour_name', 'tour')

    content = RichTextField()
    tour = models.ForeignKey(Tour,related_name="tourdetails", on_delete=models.CASCADE) # related: hỗ trợ truy vấn ngược
    tags = models.ManyToManyField('Tag', related_name="tourdetails", blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Interaction(ItemBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    tour_name = models.ForeignKey(TourDetail, on_delete=models.CASCADE, null=False)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255, null=False)


class Like(Interaction):
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'tour_name')


class Rating(Interaction):#Muc do yeu thich
    rate = models.SmallIntegerField(default=0)

