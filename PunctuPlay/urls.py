
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('quiz/', include('quiz.urls')),
    path('materi/', include('materi.urls')),
    path('', views.index)
]
