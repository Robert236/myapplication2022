from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Applicationpapers, Messages, CustomUser, Applicant, Skills, Jobs
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def fields_not_empty(current_post):
    for field in current_post:
        if current_post[field] == '':
            return False
    return True


def register_user(request):
    if request.method == 'POST':
        new_custom_user = {}
        for entry in request.POST:
            new_custom_user[entry] = request.POST[entry]
        del new_custom_user['csrfmiddlewaretoken']
        rv = fields_not_empty(new_custom_user)
        if rv:
            custom_user = CustomUser(username=new_custom_user['benutzername'],
                                     first_name=new_custom_user['vorname'],
                                     last_name=new_custom_user['nachname'],
                                     email=new_custom_user['email'],
                                     anrede=new_custom_user['anrede'],
                                     unternehmen=new_custom_user['unternehmen'],
                                     plz=new_custom_user['plz'],
                                     ort=new_custom_user['ort'])
            custom_user.save()
            note = 'Es hat sich {} neu registriert.'.format(new_custom_user['benutzername'])
            notification = Messages(titel='Neue Registrierung',
                                    nachricht=note,
                                    send_date=timezone.now(),
                                    besucher_id=CustomUser.objects.last().id,
                                    bewerber_id=1)
            notification.save()
            messages.success(request, 'Die Regestrierung wurde eingereicht!'
                                      ' Sie bekommen ein Passwort nach der '
                                      'Überprüfung zugeschickt.')
        else:
            messages.info(request, 'Bitte füllen Sie alle Felder aus.')
    context = {}
    return render(request, 'myapplication/login.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('myapplication:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('benutzername')
            password = request.POST.get('passwort')
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('myapplication:index')
            else:
                messages.info(request, 'Username oder Passwort ist nicht richtig!')
    context = {}
    return render(request, 'myapplication/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('myapplication:login_page')


@login_required(login_url='myapplication:login_page')
def index(request):
    applicant = Applicant.objects.first()
    context = {'applicant_object': applicant}
    return render(request, 'myapplication/index.html', context)


@login_required(login_url='myapplication:login_page')
def application_documents(request):
    all_documents = Applicationpapers.objects.all()
    context = {'all_documents': all_documents}
    return render(request, 'myapplication/application_documents.html', context)


@login_required(login_url='myapplication:login_page')
def document_view(request, document):
    rv_requested_document = Applicationpapers.objects.filter(bezeichnung=str(document))
    context = {}
    if rv_requested_document:
        context['current_documents'] = rv_requested_document
        return render(request, 'myapplication/document.html', context)
    else:
        return render(request, 'myapplication/ups.html', context)


@login_required(login_url='myapplication:login_page')
def contact(request):
    if request.method == 'POST':
        new_message = {}
        for entry in request.POST:
            new_message[entry] = request.POST[entry]
        del new_message['csrfmiddlewaretoken']
        rv = fields_not_empty(new_message)
        if rv:
            save_message_object = Messages(titel=new_message['titel'],
                                           nachricht=new_message['nachricht'],
                                           send_date=timezone.now(),
                                           besucher_id=request.user.id,
                                           bewerber_id=1)
            save_message_object.save()
            messages.info(request, 'Die Nachricht wurde erfolgreich versendet!')
        else:
            messages.info(request, 'Bitte alle Felder ausfüllen!')
    context = {}
    return render(request, 'myapplication/contact.html', context)


@login_required(login_url='myapplication:login_page')
def skills(request):
    applicant = Applicant.objects.first()
    personal_skills = Skills.objects.all()
    context = {'object_applicant': applicant,
               'object_personal_skills': personal_skills}
    return render(request, 'myapplication/skills.html', context)


@login_required(login_url='myapplication:login_page')
def jobs(request):
    rv_jobs = Jobs.objects.all()
    context = {'object_jobs': rv_jobs}
    return render(request, 'myapplication/jobs.html', context)
