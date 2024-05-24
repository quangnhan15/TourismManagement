from django.contrib import admin
from django.db.models import Count
from django.contrib.auth.models import Permission
from django.template.response import TemplateResponse
from django.urls import path
from django import forms
from django.utils.html import mark_safe
from .models import Category, Tour, TourDetail, Tag, User
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class TourDetailForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = TourDetail
        fields = '__all__'      #tạo ra form cho phép tương tác ất cả các fields các trường trong tourdetail riêng trường content lấy ckeditor


class TourDetailTagInline(admin.TabularInline):
    model = TourDetail.tags.through


class TourDetailAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('/static/css/main.css',)
        }

    form = TourDetailForm
    list_display = ["id", "tour_name", "created_date", "active", "tour"]
    search_fields = ["tour_name", "created_date", "tour__tour_name"]
    list_filter = ["tour_name", "tour__tour_name"]
    inlines = (TourDetailTagInline, )


class TourDetailInline(admin.StackedInline):
    model = TourDetail
    pk_name = 'tour'


class TourAdmin(admin.ModelAdmin):
    inlines = (TourDetailInline, )
    list_display = ['id', 'tour_name', 'description']
    readonly_fields = ['avatar']

    def avatar(self, obj):
        if obj:
            return mark_safe(
                '<img src="/static/{url}" alt="{alt}" width="120px />'.format(url=obj.image.name, alt=obj.tour_name)
            )


class TourAppAdminSite(admin.AdminSite):
    site_header = 'HE THONG QUAN LY TOUR DU LICH'

    def get_urls(self):
        return [
            path('tour-stats/', self.tour_stats)    #Truy cập vào đây sẽ vào hàm tour_stats
        ] + super().get_urls()      #Phép nối 2 danh sách

    def tour_stats(self, repuest):
        tour_count = Tour.objects.count()
        stats = Tour.objects.annotate(tourdetail_count=Count('tourdetails')).values("id", "tour_name", "tourdetail_count")

        return TemplateResponse(repuest, 'admin/tour-stats.html', {
            'tour_count': tour_count,
            'stats': stats
        })

# admin_site = TourAppAdminSite('mytour')

# Register your models here.
admin.site.register(Category)
admin.site.register(Tour, TourAdmin)
admin.site.register(TourDetail, TourDetailAdmin)
admin.site.register(User)
admin.site.register(Permission)
admin.site.register(Tag)
# admin_site.register(Category)
# admin_site.register(Tour, TourAdmin)
# admin_site.register(TourDetail, TourDetailAdmin)