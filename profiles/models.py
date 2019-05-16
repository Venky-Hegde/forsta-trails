# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from usermanagement.models import Base
from company.models import Company
from django.contrib.postgres.fields import JSONField
import os

def get_profile_path(instance, associated_profile_path):
    # ext = filename.split('.')[-1]  # extention
    return os.path.join('media/', associated_profile_path)


class Profile(Base):
    #id=models.IntegerField(primary_key=True,auto_created=True)
    candidate_name = models.CharField(max_length=250)
    candidate_email = models.EmailField(max_length=250, )
    phone_number= models.CharField(max_length=25, null=False)
    primary_skills = JSONField(models.CharField(), blank=True, null=True)
    experience = models.CharField(max_length=5,null=True)
    current_ctc=models.CharField(max_length=8,null=True)
    expected_ctc = models.CharField(max_length=8,null=True)
    percent_rise = models.CharField(max_length=2,null=True)
    current_company = models.CharField(max_length=250, blank=True, null=True)
    notice_period = models.CharField(max_length=3,null=True)
    resume_path = models.FileField(upload_to=get_profile_path,null=True)
    resume_name=models.CharField(max_length=1000,null=True)
    added_for=models.ForeignKey(Company,null=True)
    latest = models.BooleanField(default=True)
    extracted_words=JSONField(models.CharField(), blank=True, null=True)
    location=models.CharField(max_length=30,null=True)
    ready_for_change=models.NullBooleanField(null=True)
    attached = models.BooleanField(default=False)
    availability=models.CharField(max_length=4,null=True,default="No")
    notes = models.CharField(max_length=1000,null=True)
    current_role = models.CharField(max_length=250,default="",null=True)
    alternate_phone_number = models.CharField(max_length=15,null=True)
    is_interviewer = models.BooleanField(default=False)
    interview_skills = JSONField(models.CharField(), blank=True , null=True)
class Meta:
    ordering = ('-updated_on',)


class UnextractedProfile(models.Model):
    resume_name=models.CharField(max_length=250)

