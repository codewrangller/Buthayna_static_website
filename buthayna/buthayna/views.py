from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .contact import ContactMeForm
from django.contrib import messages



# Create your views here.
def index(request):
    return render(request, 'index.html')


def home(request):
    form = ContactMeForm()

    if request.method == 'POST':
        form = ContactMeForm(request.POST)
        if form.is_valid():
            # form.save()
            # send_mail(subject, message[fname, lname, email, phonenumber, subject, message], sender, recipient)

            subject = "Contact form inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name':form.cleaned_data['last_name'],
                'email': form.cleaned_data['emailid'],
                'phonenumber': form.cleaned_data['phone_number'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }

            message = '\n'.join(body.values())

            sender = form.cleaned_data['emailid']
            recipient = ['newrecruit38@gmail.com']

            try:
                send_mail(subject, message, sender, recipient, fail_silently=True)

            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            messages.success(request, "Your response has been submited successfully.")
            return redirect ('/')
        else:
            messages.error(request, "Error. Message not sent.")
    context = {
        'form':form,
    }
    return render(request, "email.html", context)
