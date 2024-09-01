
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path("admin/", admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path("", include('retail.urls')),
    path("api/", include('api.urls')),
    path('silk/', include('silk.urls', namespace='silk'))
]


from django.conf import settings
from django.conf.urls import include
from django.urls import path


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns