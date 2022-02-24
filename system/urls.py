"""system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bookclub import views
from bookclub.views import account_views, authentication_views, dashboard_views, club_related_views, book_views, club_views, user_views, search_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.landing_page, name='landing_page'),
    path('users/', user_views.UsersListView.as_view() , name = 'user_list'),
    path('clubs/', club_views.ClubsListView.as_view() , name = 'club_list'),
    path('books/', book_views.BooksListView.as_view() , name = 'book_list'),
    path('sign_up/', authentication_views.sign_up, name='sign_up'),
    path('log_in/', authentication_views.LogInView.as_view(), name='log_in'),
    path('log_out/', authentication_views.log_out, name='log_out'),
    path('home/', dashboard_views.home_page, name='home'),
    path('password/', account_views.PasswordView.as_view(), name='password'),
    path('profile/', account_views.user_profile, name='profile'),
    path('profile/edit/', user_views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('applications/', club_related_views.ApplicationsView.as_view(), name='applications'),
    path('applications/accept/<int:pk>/', club_related_views.app_accept, name='app_accept'),
    path('applications/remove/<int:pk>/', club_related_views.app_remove, name='app_remove'),
    path('new_application/<int:club_id>/', club_related_views.new_application, name='new_application'),
    path('club_profile/<int:club_id>/', club_views.club_profile, name='club_profile'),
    path('club_profile/<int:club_id>/meetings', club_related_views.meetings_list, name='meetings_list'),
    path('user_profile/<int:user_id>/', user_views.user_profile, name='user_profile'),
    path('book_profile/<int:book_id>/', book_views.ShowBookView.as_view(), name='book_profile'),
    path('my_clubs/', club_views.club_selector, name='club_selector'),
    path('my_clubs1/', club_views.club_selector_alt, name="club_selector_alt"),
    path('my_applications/', club_related_views.MyApplicationsView.as_view(), name='my_applications'),
    path('new_club/', club_views.new_club, name='new_club'),
    path('club_profile/<int:pk>/meeting/', club_related_views.MeetingScheduler.as_view(), name='schedule_meeting'),
    path('search/', search_views.search, name='search_page'),
    path('leave_club/<int:club_id>/', club_views.leave_club, name='leave_club')
]
