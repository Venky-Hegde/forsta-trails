# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Create your models here.
from django.db import models


class Company(models.Model):

    company_name = models.CharField(max_length=250,null=False)
    level = models.SmallIntegerField(null=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('usermanagement.User', related_name='created_companies',null=True)
    updated_by = models.ForeignKey('usermanagement.User', related_name='updated_companies',null=True)
    parent_company=models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    interview_services = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

