from django.urls import path
from .views import(
    AdminPanelUserView,
    AdminPanelFilesView,
    AdminPanelFileManageView,
    rice_upload
)

app_name = 'profiles'

urlpatterns = [
    path('user_management/', AdminPanelUserView.as_view(), name='user-manage'),
    path('file_management/', AdminPanelFileManageView.as_view(), name='file-manage'),
    path('file_upload/', AdminPanelFilesView.as_view(), name='file_upload'),
    path('rice/upload/', rice_upload, name='rice_upload'),

]
