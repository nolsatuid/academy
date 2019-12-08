from django.urls import path
from . import views

app_name = "inbox"
urlpatterns = [
    path('', views.GetInboxList.as_view(), name='inbox'),
    path('<int:id>', views.InboxDetail.as_view(), name='inbox_detail'),
    path('read', views.BulkReadUnread.as_view(), name='inbox_read'),
]
