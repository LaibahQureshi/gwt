from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit/', views.submit_view, name='submit'),
    path('all-progress/', views.all_progress_view, name='all_progress'),
    path('delete/<int:update_id>/', views.delete_update, name='delete_update'),
    path('set-goal/', views.set_goal, name='set_goal'),
    path('create-subcategory/', views.create_subcategory, name='create_subcategory'),

]
