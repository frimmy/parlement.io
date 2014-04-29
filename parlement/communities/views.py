from django.shortcuts import render
from django.http import HttpResponseRedirect 
from django.core.mail import send_mail
from django.contrib import messages
from django.core.urlresolvers import reverse

from .models import Community, JoinRequest


def list(req):
    communities = Community.objects.all()
    return render(req,'communities/list.html',
        {'communities':communities})

def view(req, name):
    community = Community.objects.get(name=name)
    if req.user not in community.members.all():
        return HttpResponseRedirect(community.get_join_url())
    return render(req,'communities/one.html', 
        {'community':community})

def join(req, name):
    community = Community.objects.get(name=name)
    email = req.POST.get('email','')

    if req.method == "POST":
        if community.is_email_valid(email):
            token = JoinRequest.generate(community, email)
            send_mail('[parlement.io] Confirmation to join %s' % community.name,
                'To join this community, you need to follow'
                '<a href="%s">this link' % reverse('communities:validate_join', args=(token.token,)),
                'no-reply@parlement.io',
                [email], fail_silently=False)
            messages.add_message(req, messages.SUCCESS, 'Email sent to %s' % email)
        else:
            messages.add_message(req, messages.ERROR, 'Invalid email')
    return render(req,'communities/join.html', 
        {'email':email, 'community':community})

def validate_join(req, token):
    request = JoinRequest.objects.get(token=token)
    community = request.community
    if hashed_email not in community.members_emails:
        community.add_member(req.user, hashed_email)
        messages.add_message(req, messages.SUCCESS, 'You joined %s' % community.name)
        return HttpResponseRedirect(req, reverse('communities:view',args=(community.name))) 
    messages.add_message(req, messages.SUCCESS, 
        'This email was already used to join this community ' % community.name)
    return HttpResponseRedirect(req, reverse('communities:list'))
