# -*- coding: utf-8 -*-


from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from company.models import Company

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    company = models.ForeignKey(Company, related_name='companyname', null=True)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=256)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    short_name = models.CharField(max_length=2, null=True)
    phone_number = models.CharField(max_length=15, blank=False, null=True)
    is_super_user = models.BooleanField(default=False)  # A Super User
    is_operator = models.BooleanField(default=False)  # A company's operator
    is_company = models.BooleanField(default=False)  # A company's user
    created_dt = models.DateField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now_add=True, null=True)
    primary_user = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        a=self.first_name[:1] + self.last_name[:1]
        return a

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
    def get_company_count(self):

        customer_count=Company.objects.filter(created_by_id = self.id).count()

        return customer_count


    def get_job_count(self):
        from jobs.models import Job
        job_cont=Job.objects.filter(company_id=self.company_id).count()

        return  job_cont

    def get_profile_count(self):
        from jobs.models import JobProfileAssociation
        profile_count=JobProfileAssociation.objects.filter(company_id=self.company_id).count()

        return  profile_count

    def get_chat_count(self):
        from jobs.models import Conversation
        chat_count= Conversation.objects.filter(resume_id=self.resume_id,job_id=self.job_id,read_status = False).count()
        return chat_count

    # def get_time(self):
    #     from profiles.models import Profile
    #     profiles = Profile.objects.filter(id=self.id)
    #     return (month.length > 1 ? month: "0" + month) + "/" + date.getDate() + "/" + date.getFullYear();
    def get_total_company_count(self):
        customer_count=Company.objects.filter(parent_company_id = self.company_id).count()
        return customer_count
class Base(models.Model):
    """
    This is a Base Class Common across all models
    """


    created_dt = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, related_name='%(class)s_created_by', null=True)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated_by', null=True)


    class Meta:
        abstract = True



class Messages(models.Model) :
    msg_id  = models.SmallIntegerField(null=True)
    message = models.CharField(max_length=500 , null=True)



