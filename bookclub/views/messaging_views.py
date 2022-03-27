from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from bookclub.templates import *
from bookclub.forms import *
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from bookclub.models import *
from django.views.generic.edit import View
from django.db.models import Q
from notifications.signals import notify


# Adapted from https://legionscript.medium.com/building-a-social-media-app-with-django-and-python-part-14-direct-messages-pt-1-1a6b8bd9fc40
class CreateChatView(View):

    def get(self, request, *args, **kwargs):
        form = ChatForm()
        context = {
            'form': form
        }
        return render(request, 'create_chat.html', context)

    def post(self, request, *args, **kwargs):
        form = ChatForm(request.POST)
        email = request.POST.get('email')
        try:
            receiver = User.objects.get(email=email)
            if Chat.objects.filter(user=request.user, receiver=receiver).exists():
                chat = Chat.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('chat', pk=chat.pk)

            if form.is_valid():
                sender_chat = Chat(
                    user=request.user,
                    receiver=receiver
                )
                sender_chat.save()
                messages.add_message(request, messages.SUCCESS, "Chat created!")
                chat_pk = sender_chat.pk
                return redirect('chat', pk=chat_pk)
        except:
            return redirect('create_chat')

def createChatFromProfile(request, user_id):
    try:
        receiver = User.objects.get(id=user_id)
        if Chat.objects.filter(user=request.user, receiver=receiver).exists():
            chat = Chat.objects.filter(user=request.user, receiver=receiver)[0]
            return redirect('chat', pk=chat.pk)

        sender_chat = Chat.objects.create(
            user=request.user,
            receiver=receiver
        )
        messages.add_message(request, messages.SUCCESS, "Chat created!")
        chat_pk = sender_chat.pk
        return redirect('chat', pk=chat_pk)
    except:
        return redirect('create_chat')


# Adapted from https://legionscript.medium.com/building-a-social-media-app-with-django-and-python-part-14-direct-messages-pt-1-1a6b8bd9fc40
class ListChatsView(View):

    def get(self, request, *args, **kwargs):
        chats = Chat.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        context = {
            'chats': chats
        }
        return render(request, 'inbox.html', context)


# Adapted from https://legionscript.medium.com/building-a-social-media-app-with-django-and-python-part-14-direct-messages-pt-1-1a6b8bd9fc40
class CreateMessageView(View):

    def post(self, request, pk, *args, **kwargs):
        chat = Chat.objects.get(pk=pk)
        if chat.receiver == request.user:
            receiver = chat.user
        else:
            receiver = chat.receiver
        message = Message(
            chat=chat,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message'),
        )

        notify.send(
            request.user,
            recipient=receiver,
            verb = 'sent you a message',
            target=message,
            action_object=message,
                )
        message.save()
        return redirect('chat', pk=pk)

    def get(self, request, msg_id):
        message = Message.objects.get(id=msg_id)
        current_user = request.user
        if message.msg_to_id == current_user.id:
            message.is_read = True
            message.save()
       


# Adapted from https://legionscript.medium.com/building-a-social-media-app-with-django-and-python-part-14-direct-messages-pt-1-1a6b8bd9fc40
class ChatView(View):

    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        chat = Chat.objects.get(pk=pk)
        message_list = Message.objects.filter(chat__pk__contains=pk)
        context = {
            'chat': chat,
            'form': form,
            'message_list': message_list
        }
        return render(request, 'chat.html', context)
