from django.contrib import admin
from django.urls import path, include
from miniipip.views import redirect_root,privacy
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', redirect_root),
    path('miniipip/', include('miniipip.urls'), ),
    path('privacy',privacy)
]
