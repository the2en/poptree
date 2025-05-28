from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
import os

urlpatterns = [
    path('status/', views.get_tree_status, name='tree-status'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=os.path.join(settings.BASE_DIR, 'trees', 'static')
    )