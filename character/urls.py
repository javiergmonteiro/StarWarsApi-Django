from django.urls import path, re_path
from . import views
from django.conf.urls import url


app_name = 'character'

urlpatterns = [
    path('<int:pk>/', views.CharacterDetail.as_view(), name="get_character"),
    path('<int:pk>/rating/', views.CharacterRating.as_view({'post':'rate'}), name="post_rating")
]