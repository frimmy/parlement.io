from django.db import models
from django.conf import settings 
from django.core.urlresolvers import reverse

import re, hashlib, random

#SHA1_RE = re.compile('^[a-f0-9]{40}$')

#email_regex = r'^[a-z]{8}@etu.utc.fr$'

class Community(models.Model):
    name = models.SlugField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    email_regex = models.CharField(max_length=400)
    join_help = models.CharField(max_length=300)
    members_emails = models.TextField(blank=True)

    def add_user(self, user):
        self.members.add(user)
        self.save()

    def add_email(self, email):
        self.members_emails += email+'\n'
        self.save()
    
    def mail_can_join(self, mail):
        return mail not in self.members_emails

    def is_email_valid(self, email):
        return re.match(self.email_regex, email) != None 

    def get_join_url(self):
        return reverse('communities:join',args=(self.name,))
    
    def get_absolute_url(self):
        return reverse('communities:view',args=(self.name,))

    def __str__(self):
        return self.name

class JoinRequest(models.Model):
    community = models.ForeignKey(Community)
    token = models.CharField(max_length=40, unique=True, primary_key=True)
    hashed_email = models.CharField(max_length=400)
    date = models.DateField(auto_now=True)

    def generate(community, mail):
        token = JoinRequest()
        token.token = hashlib.sha1(str(random.SystemRandom().random()).encode('utf-8')).hexdigest()
        token.community = community
        token.hashed_email = hashlib.sha1(mail.encode('utf-8')).hexdigest()
        token.save()
        return token

