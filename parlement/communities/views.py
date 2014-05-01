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
                'To join this community, you need to follow '
                '<a href="%s">this link</a>' % 
                    req.build_absolute_uri(reverse('communities:validate_join', args=(token.token,))),
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
    if community.mail_can_join(request.hashed_email) and req.user not in community.members.all():
        community.add_user(req.user)
        community.add_email(request.hashed_email)
        messages.add_message(req, messages.SUCCESS, 'You joined %s' % community.name)
    else:
        messages.add_message(req, messages.WARNING, 'You already joined %s' % community.name)
    return HttpResponseRedirect(reverse('communities:view',args=(community.name,)))
