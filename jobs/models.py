# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField

from company.models import Company
from usermanagement.models import Base,User
from profiles.models import Profile
import os


class Status(Base):

   status = models.CharField(max_length=20)
   future_state = models.SmallIntegerField(null=True)
   level = ArrayField(models.IntegerField(),null=True)
   status_value = models.SmallIntegerField(null=True)
def default_date():
    today=datetime.datetime.now()
    s= datetime.timedelta(45)
    final_date=str(today+s).split(" ")
    return final_date[0]

class Job(Base):
    company = models.ForeignKey(Company,related_name='association_Job',null=True,on_delete=models.CASCADE)
    parent_company = models.ForeignKey(Company)
    job_description = models.CharField(max_length=3000)
    job_title=models.CharField(max_length=100,null=True)
    primary_skills = JSONField(models.CharField(), blank=True, null=True)
    lead_time = models.SmallIntegerField(blank=True, null=True)
    experience = models.CharField(max_length=5,null=True)
    no_positions = models.SmallIntegerField(null=True)
    job_status = models.ForeignKey(Status,null=True)
    created_for=models.CharField(max_length=20,null=True)
    job_seq=models.IntegerField(null=True)
    company_identifier=models.CharField(max_length=4, null=True)
    reference_id=models.CharField(max_length=10,null=True)
    job_type=models.CharField(max_length=20,null=True,default="FullTime")
    location=models.CharField(max_length=30,null=True)
    job_end_date=models.DateField(null=True,default=default_date())
    is_end_date=models.BooleanField(default=False)
    job_status_value = models.CharField(max_length=25,default="Active", null=True)



def content_associated_file_name(instance, associated_profile_path):
    # ext = filename.split('.')[-1]  # extention
    return os.path.join('media/', associated_profile_path)


class JobProfileAssociation(Base):


    job = models.ForeignKey(Job,related_name='JobProfileAssociation_job',on_delete=models.CASCADE)
    resume = models.IntegerField(null=True)
    vc_id=models.ForeignKey(Company,related_name='associated_vendor',on_delete=models.CASCADE,null=True)
    company = models.ForeignKey(Company,related_name='association_company')
    status = models.ForeignKey(Status,related_name='JobprofileAssociation_status')
    final_status = models.CharField(max_length=20,default="Shared")
    associated_profile_path =models.FileField(upload_to=content_associated_file_name,null=True)
    candidate_name=models.CharField(null=True,max_length=250)
    candidate_email=models.CharField(null=True,max_length=250)
    primary_skills=JSONField(models.CharField(), blank=True, null=True)
    phone_number= models.CharField(max_length=15, null=True)
    experience = models.CharField(max_length=5,null=True)
    current_ctc=models.CharField(max_length=8,null=True)
    expected_ctc = models.CharField(max_length=8,null=True)
    current_company = models.CharField(max_length=250, blank=True, null=True)
    notice_period = models.CharField(max_length=3,null=True)
    location=models.CharField(max_length=30,null=True)
    extracted_words=JSONField(models.CharField(), blank=True, null=True)
    cc_name=models.CharField(max_length=250,null=True)
    vc_name=models.CharField(max_length=250,null=True)
    receive_update_dt = models.DateField(null=False)
    customer_checked = models.BooleanField(default=False)
    status_remark = models.CharField(max_length=500, null=True)
    notes = models.CharField(max_length=1000 , null=True)
    msg_read_status = models.SmallIntegerField(null=True)
    next_level_status = models.CharField(max_length=250,null=True)
    current_role = models.CharField(max_length=250,default="",null=True)

class Conversation(Base):

    # job= models.ForeignKey(Job,related_name='Conversation_job',null=True)
    jpa = models.ForeignKey(JobProfileAssociation,related_name='conversation_resume',null=True,)
    conversation_to = JSONField(models.CharField(), blank=True, null=True)
    # conversation_on = models.DateTimeField(auto_now=True)
    # read_status = models.BooleanField(default=False)
    # send_to      = models.ForeignKey(Company,null=True)
    initiated_by = models.ForeignKey(User)

from django.core.exceptions import ValidationError
class Skill(models.Model):
    skill = models.CharField(null=False,max_length=100)

    def clean(self):
        if Skill.objects.filter(skill__iexact=self.skill).exists():
            raise ValidationError("Skill name already exists, type again")
    def __str__(self):
        return self.skill

class Settings(models.Model) :
    key = models.CharField(max_length=25)
    value=models.SmallIntegerField(null=False)
