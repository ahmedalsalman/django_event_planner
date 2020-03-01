from django.urls import path
from events import views

urlpatterns = [
	path('', views.home, name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('detail/<int:event_id>/', views.event_detail, name='event-detail'),
    path('detail/<int:event_id>/update/', views.event_update, name='edit'),
    path('detail/create/', views.event_create, name='create'),
    path('detail/<int:event_id>/book/', views.event_book, name='book'),
    path('find/', views.event_list, name='find-events'),


]
