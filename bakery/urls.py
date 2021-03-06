import debug_toolbar
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from user_profile.views import profile_view, admin_view, create_item_via_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('accounts/', include('allauth.urls')),
    path('accounts/admin/', admin_view, name='admin-view'),
    path('accounts/profile/', profile_view, name='profile'),
    path('accounts/create_item/', create_item_via_admin, name='create-item'),
    path('', include('items.urls', namespace='items')),
]

if settings.DEBUG:
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
