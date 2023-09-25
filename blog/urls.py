from . import views
from django.urls import path


urlpatterns = [
    # for class based views we must use as_view() for it to be rendered
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
