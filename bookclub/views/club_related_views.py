"""Club related views."""
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from bookclub.templates import *
from bookclub.forms import  ApplicantForm, ApplicationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.edit import View
from bookclub.models import User, Club, Application
from bookclub.views import club_views


class ApplicationsView(LoginRequiredMixin, View):
    """View that handles club applications."""

    http_method_names = ['get']

    def get(self, request):
        """Display application template"""
        return self.render()

    def render(self):
        current_user = self.request.user
        """Render all applications of this user's owned clubs"""     
        owned_clubs = []
        applicants = []
        for c in Club.objects.all():
            if c.owner == current_user:
                owned_clubs.append(c)
        
        for a in Application.objects.all():
            if a.club in owned_clubs:
                applicants.append(a)
                                                                                                                               
        return render(self.request, 'applications.html', {'applicants': applicants})


def app_accept(request, pk):
    """Accept application"""
    app = Application.objects.all().get(pk=pk)
    app.club.make_member(app.applicant)
    app.delete()
    messages.add_message(request, messages.SUCCESS, "User accepted!")
    club_views.club_util(request)
    return redirect('applications')

def app_remove(request, pk):
    """Reject application"""
    app = Application.objects.all().get(pk=pk)
    app.delete()
    messages.add_message(request, messages.SUCCESS, "User rejected!")
    return redirect('applications')

@login_required
def new_application(request, club_id):
    """ Create A New Application """
    form = ApplicationForm(request.POST)
    if form.is_valid():
        application = form.save() #TODO: Get the application to save into the database and get read from the applications view
        messages.add_message(request, messages.SUCCESS, f"Application to {Club.objects.get(pk=club_id).name} was successfully submitted!")
    else:
        messages.add_message(request, messages.ERROR, f"Could not apply to the following club: {Club.objects.get(pk=club_id).name}")
    return redirect('applications')

