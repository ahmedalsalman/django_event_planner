from django.urls import path
from .views import *

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('dashboard/', dashboard, name='dashboard'),
    path('detail/<int:event_id>/', event_detail, name='event-detail'),
    path('detail/<int:event_id>/update/', event_update, name='edit'),
    path('detail/create/', event_create, name='create'),
    path('detail/<int:event_id>/book/', event_book, name='book'),
    path('find/', event_list, name='find-events'),


]
