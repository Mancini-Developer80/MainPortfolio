from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse
from django.views.generic import TemplateView
import os

def serve_img(request, path):
    file_path = os.path.join(settings.BASE_DIR, 'img', path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='image/webp')
    from django.http import Http404
    raise Http404()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', TemplateView.as_view(template_name='test_img.html')),
    path('', include('pages.urls')),
    path('blog/', include('blog.urls')),
    re_path(r'^img/(?P<path>.*)$', serve_img),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
