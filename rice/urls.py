from django.urls import path
from .views import(

    HomePageView,
    DocsPageView,
    rice_list_view,
    get_data_name,
    get_data_info,
    info_view,
    advanced_search_view,
    comparison_view,
    get_data_comparison_view,
    AboutPageView
)

app_name = 'rice'

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('rice_list/',rice_list_view, name="searches"),
    path('get-data/',get_data_name),
    path('info/<int:pk>/',info_view, name="info-view"),
    path('get_data_info/<int:pk>/<str:fieldGroup>/',get_data_info, name ="data-info"),
    path('advanced_search/',advanced_search_view, name ="advanced-search"),
    path('comparison/',comparison_view, name ="comparison"),
    path('get_data_comparison/<str:fieldGroup>/',get_data_comparison_view, ),
    path('about/',AboutPageView.as_view(), name ="about"),
]
