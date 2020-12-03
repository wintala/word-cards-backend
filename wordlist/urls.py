from . import views
from django. urls import path

urlpatterns = [
    path("", views.base, name="testpoint"),
    path("vocabs/", views.VocabList.as_view(), name="vocabs"),
    path("vocabs/<str:pk>/", views.VocabDetail.as_view(), name="vocabs_detail"),
    path("pairs/", views.WordPairList.as_view(), name="pairs"),
    path("pairs/<str:pk>/", views.WordPairDetail.as_view(), name="pairs_detail"),
    path("users/", views.UserView.as_view(), name="users"),
    path("login/", views.login, name="login"),
]
