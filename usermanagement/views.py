# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.db.models.functions import Lower

import textract
from io import StringIO

import xlwt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from usermanagement.decorators import user_permission,is_company,is_operator
from usermanagement.models import Messages
from usermanagement.utils import generate_secretkey, authenticate_key
from smartrec.settings import base, os
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from smartrec.settings import base

User = get_user_model()
from company.models import Company
from jobs.models import Job
from profiles.models import Profile
from django.db.models import Q
import json
from django.http import JsonResponse
from jobs.models import JobProfileAssociation, Conversation
import datetime
import pandas as pd
from datetime import date, timedelta

from django.http import HttpResponse

class Landingscreen(View):
    def get(self,request):
        return render(request,"Login.html")

class Log_screen(View):
    def post(self,request):
        return render(request,"Login.html")

# To get message from db
def get_message(id) :
    print("comming here")
    msg = Messages.objects.filter(msg_id = id).values_list("message").first()
    print((msg))
    return msg



# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class Login_User(View):
    def get(self, request):
        if request.user is not None and request.user.is_anonymous() == False:
             user = request.user
             if user.is_super_user:
                 return HttpResponseRedirect(reverse('operatorlist'))
             elif user.is_operator:
                 return HttpResponseRedirect(reverse('operatorpage'))
             return HttpResponseRedirect(reverse("customerpage"))
        return render(request, 'Login.html')

    def post(self, request):
        try :
            print("inside try")
            user=User.objects.get(email = request.POST.get('username') , is_active = False)
            print(user)
            data = {"error" : get_message(1)}

            return JsonResponse(data , safe=False)
        except :
            print("here")
            user = authenticate(email=request.POST.get('username', None).lower(), password=request.POST.get('password', None))
            print(user)
            if user is not None:

                login(request, user)
                if user.is_super_user:
                    data = {"msg": "admin"}
                    return JsonResponse(data, safe=False)
                if user.is_operator:
                    data = {"msg" : "operator"}
                    return JsonResponse(data , safe=False)
                data = {"msg": "customer"}
                return JsonResponse(data, safe=False)
            else:

                data = {"error": get_message(2),}
                return JsonResponse(data , safe=False)


login_user = Login_User.as_view()


# when admin log in creating operators
@method_decorator(user_permission, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class OperatorList(LoginRequiredMixin, View):
    # permission_classes=(IsAuthenticated,IsSuperUser)


    def get(self, request):
        operators = User.objects.filter(is_operator=True)
        context = {'operators': operators}
        return render(request, 'Operatorlist.html', context)


    def post(self, request, *args, **kwargs):
        print(request.POST, "this is post data")
        try:
            Com = Company.objects.get(company_name=request.POST.get('company_name'), level=1)

            data = {"msg": get_message(3)}
            return JsonResponse(data, safe=False)

        except Exception:

            Com = Company.objects.create(id=request.user.company_id,
                                        company_name=request.POST.get('company_name'),
                                        level=1,
                                        created_by_id=request.user.id, updated_by_id=request.user.id,
                                        interview_services =request.POST.get("Interviewer_service"))
        try:
            email = User.objects.get(email=request.POST.get('email').lower())

            data = {"msg": get_message(4)}
            return JsonResponse(data, safe=False)

        except Exception:

            user = User.objects.create(first_name=request.POST.get('first_name'),
                                       last_name=request.POST.get('last_name'),
                                       email=request.POST.get('email').lower(),
                                       phone_number=request.POST.get('phone_number'),
                                       company=Com,
                                       is_operator=True,
                                       primary_user = True,

                                            )
            # password = User.objects.make_random_password(length=15, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789')
            user.set_password(request.POST.get('password'))
            user.save()

        data = {"msg": get_message(5)}
        return JsonResponse(data, safe=False)


operator = OperatorList.as_view()


# for checking already exits company (Operator)
@method_decorator(csrf_exempt, name='dispatch')
class Checkcompanyoperator(View):
    def post(self, request):
        status = True
        print(request.user.id)
        company_name = Company.objects.filter(company_name__icontains=request.POST.get('company_name'), level=1).first()
        print(company_name)
        print(request.POST.get('company_name'))
        if hasattr(company_name, "company_name"):
            status = False

        else:
            status = True

        print(status)
        return HttpResponse(json.dumps({"status": status}))


# when operator log in and creating customers......
@method_decorator(is_operator, name='dispatch')

class Customers(LoginRequiredMixin, View):
    # permission_classes=(IsAuthenticated,IsOperator)


    def get(self, request):
        company = Company.objects.filter(parent_company_id=request.user.company_id).values_list("id", flat=True)
        print("comming here........................................................")

        profiles = Profile.objects.filter(added_for_id=request.user.company_id, latest=True , is_interviewer=True).order_by(('-updated_on'))
        print(profiles, 'sorted profiles')
        companyid = request.GET.get('company_id')
        jobid = request.GET.get('jobid')
        customers = User.objects.filter(company_id__in=list(company)).order_by('-updated_on')
        detail = User.objects.filter(company_id=request.user.company.id).order_by('-updated_on')
        print(detail, "list of company operators")
        context = {'customers': customers, 'data': profiles, "x": "True","details": detail}

        return render(request, 'customerlist.html', context)


    def post(self, request, *args, **kwargs):

        user = User()
        company_name = request.POST.get('company_name')


        try:

                if request.user.company.company_name == company_name:

                    return HttpResponseRedirect("customerlist.html")



                elif Company.objects.get(company_name=request.POST.get('company_name'),
                                         created_by_id=request.user.id):

                    return HttpResponseRedirect("customerlist.html")






        except Exception:
            Com = Company.objects.create(company_name=request.POST.get('company_name'), level=2,
                                            created_by_id=request.user.id, updated_by_id=request.user.id,
                                            parent_company_id=request.user.company.id)
        try:
            email = User.objects.get(email=request.POST.get('email').lower())
            company = Company.objects.filter(parent_company_id=request.user.company_id).values_list("id", flat=True)
            customers = User.objects.filter(company_id__in=list(company))
            profiles = Profile.objects.filter(added_for_id=request.user.company_id, latest=True).order_by('-updated_on')
            context = {'customers': customers, 'data': profiles, "x": "True", "success": "False"}
            print("ccccccccccccccccccccccccc.....................................")
            return render(request, 'customerlist.html', context)


        except Exception:

            user = User.objects.create(first_name=request.POST.get('first_name'),
                                           last_name=request.POST.get('last_name'),
                                           email=request.POST.get('email').lower(),
                                           phone_number=request.POST.get('phone_number'),
                                           company=Com,
                    is_company=True, short_name=request.user.get_short_name()
                                           )

            password = User.objects.make_random_password(length=15,
                                                             allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789')
            user.set_password(request.POST.get('password'))

            user.save()
            return HttpResponseRedirect("customerlist.html")


        return HttpResponseRedirect("customerlist.html")

customers = Customers.as_view()


#when operator log in creating users..........
@method_decorator(csrf_exempt, name='dispatch')
class AddOperator(View):
    def post(self,request) :
        Com = Company.objects.filter(company_name=request.user.company.company_name).first()
        user = User.objects.create(first_name=request.POST.get('first_name'),
                                   last_name=request.POST.get('last_name'),
                                   email=request.POST.get('email').lower(),
                                   phone_number=request.POST.get('phone_number'),
                                   company=Com,
                                   is_operator=True,
                                   short_name=request.POST.get('first_name')[:1] + request.POST.get('last_name')[:1],
                                   )
        user.set_password(request.POST.get('password'))

        user.save()
        data= {"msg" : get_message(5)}
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class Checkcompany(View):
    def post(self, request):
        print("working.....................")
        status = False
        print(request.user.id)
        company_name = Company.objects.filter(company_name__icontains=request.POST.get('company_name'),
                                              created_by_id=request.user.id).first()
        print(company_name)
        print(request.POST.get('company_name'))
        if hasattr(company_name, "company_name"):
            status = False
        elif request.user.company.company_name == request.POST.get('company_name').lower():
            status = False

        else:
            status = True

        print(status)
        return HttpResponse(json.dumps({"status": status}))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


logout_user = LogoutView.as_view()

# when customer creating job....................

@method_decorator(is_company, name='dispatch')
class CreateJob(LoginRequiredMixin, View):
    # permission_classes=(IsAuthenticated,IsCustomer)


    def get(self, request):
        jobsq = Job.objects.filter(company_id=request.user.company_id)
        jobsw = Job.objects.filter(created_by_id=request.user.id)
        data = {'jobs': jobsq | jobsw}
        print(data)
        return render(request, 'jobs.html', data)


    def post(self, request):
        print(" i am customer,.............................................................")
        print(request.user.company.company_name)
        print(request.user.company.id)
        job_mail=request.POST.get("job_mail")
        print(job_mail,"&&&&&&&&&&&&&&&&&&")
        job_end = request.POST.get("job_end_date")
        print(job_end,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@.......................")
        date1 = change_date_format(job_end)
        primary_skills=request.POST.get("primaryskills").split(',')


        job_count = Job.objects.filter(company_id=request.user.company.id).count()
        print(job_count)

        if job_end is "":
            jobs = Job.objects.create(job_description=request.POST.get("jobdescription"),
                                      job_title=request.POST.get("jobtitle"),
                                      primary_skills=request.POST.get("primaryskills"),
                                      lead_time=request.POST.get("leadtime"),
                                      experience=request.POST.get("experience"),
                                      no_positions=request.POST.get("positions"),
                                      created_for=request.POST.get("createdfor"),
                                      reference_id=request.POST.get("reference_id"),
                                      job_type=request.POST.get("job_type"),
                                      company_id=request.user.company.id,
                                      parent_company_id=request.user.company.parent_company_id,
                                      created_by_id=request.user.id,
                                      company_identifier=request.user.company.company_name[:3] + "-",
                                      job_seq=job_count + 1,
                                      location=request.POST.get("location"),

            )
            jobs.save()

        else:
            jobs = Job.objects.create(job_description=request.POST.get("jobdescription"),
                                      job_title=request.POST.get("jobtitle"),
                                      primary_skills=request.POST.get("primaryskills"),
                                      lead_time=request.POST.get("leadtime"),
                                      experience=request.POST.get("experience"),
                                      no_positions=request.POST.get("positions"),
                                      created_for=request.POST.get("createdfor"),
                                      reference_id=request.POST.get("reference_id"),
                                      job_type=request.POST.get("job_type"),
                                      company_id=request.user.company.id,
                                      parent_company_id=request.user.company.parent_company_id,
                                      created_by_id=request.user.id,
                                      company_identifier=request.user.company.company_name[:3] + "-",
                                      job_seq=job_count + 1,
                                      location=request.POST.get("location"),
                                      job_end_date=date1,

                                      )
            jobs.save()

        skills = Skill.objects.all().values_list("skill")
        skill_set = [skill[0] for skill in skills]
        skils_count = Skill.objects.all().count() + 1
        print(skils_count)

        print(skill_set, "vvvvvvvvvvvvvvvvvvvvvvccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc")
        add_skils = [skil for skil in primary_skills if skil not in skill_set]
        for add_skill in add_skils:
            Skill.objects.create(id=skils_count, skill=add_skill)
            skils_count = skils_count + 1

        print(add_skils, "aaaaaaaaaaaaaaaasssssssssssssddddddddddddddddddddddddffffffffffffffffffffffff")
        return HttpResponseRedirect("customerlist.html")


customerpage = CreateJob.as_view()


@method_decorator(csrf_exempt, name='dispatch')
class OperatorsJobListing(LoginRequiredMixin, View):
    def get(self, request, companyid):
        print(companyid, "this is cid")
        print(type(companyid))
        if companyid is '0':
            jobs = Job.objects.filter(parent_company_id=request.user.company.id).values('job_description', 'id',
                                                                                        'job_title', 'primary_skills',
                                                                                        'lead_time', 'experience',
                                                                                        'created_for').order_by('-updated_on')
            data = {'jobs': list(jobs)}
        else:

            c_name = Company.objects.filter(id=companyid).first().company_name
            print(c_name)
            jobs = Job.objects.filter(company_id=companyid).values('job_description', 'id', 'job_title',
                                                                   'primary_skills',
                                                                   'lead_time', 'experience', 'created_for').order_by('-updated_on')
            data = {'jobs': list(jobs), "pk": companyid, "c_name": c_name}

        return JsonResponse(data, safe=False)




operatorsJobListing = OperatorsJobListing.as_view()

class CompanyJoblist(View):
    def get(self,request):
        print(request.GET.get("com_id") , "ccccccccccccccccciiiiiiiiiiiiiiddddddddddddd")
        companyid=request.GET.get("com_id")
        if (companyid is '0'):
            jobs = Job.objects.filter(parent_company_id=companyid).values('id', 'job_title').order_by('-updated_on')
        else :
            jobs = Job.objects.filter(company_id=companyid).values( 'id', 'job_title').order_by('-updated_on')
        print((jobs , "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))
        data = {"jobs" : list(jobs)}
        return JsonResponse(data, safe=False)

# when operator log in and creating job for customers...........

import json
import datetime
@method_decorator(csrf_exempt, name='dispatch')
class OperatorsJob(LoginRequiredMixin, View):
    def get(self, request, companyid):

        c_name = Company.objects.filter(id=companyid).first().company_name
        print(c_name, "this is company name")
        job_type=request.GET.get("job_type")
        print(job_type,"&&&&&&&&&&&&&&&&&")
        jobs = Job.objects.filter(company_id=companyid)
        data = {'jobs': jobs, "pk": companyid, "c_name": c_name}
        return render(request, 'operatorjobs.html', data)

    def post(self, request, *args, **kwargs):
        print(request.POST, ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>jjjjjjjjjjjjjjjjjjjjjjjjjjj")
        c_name = Company.objects.filter(id=request.POST.get("companyid_job")).first().company_name
        print(c_name,"$$$$$$$$$$$$$$$")
        job_count = Job.objects.filter(company_id=request.POST.get("companyid_job")).count()
        print("ghgdghcgjhgjhngvjhnjnvnghnfghjfghfghngn................................................")
        print(c_name)
        print(request.user.company_id)
        print(request.POST.get("companyid_job"))
        com_id = request.POST.get("companyid_job")
        email_list = [request.POST.get("job_mail")]
        print(email_list,"$$$$$$$$_----------------")
        primary_skills=request.POST.get("primaryskills").split(',')
        print(primary_skills)
        job_end=request.POST.get("job_end_date")
        print(job_end,"@@@@@@@@@@@@@@2...............")
        date1=change_date_format(job_end)
        print(date1,"######################")

        if job_end is "":
             jobs=Job.objects.create(job_description=request.POST.get("jobdescription"),
                               job_title=request.POST.get("jobtitle"),
                               primary_skills=request.POST.get("primaryskills"),
                               lead_time=request.POST.get("leadtime"),
                               experience=request.POST.get("experience"),
                               no_positions=request.POST.get("positions"),
                               created_for=request.POST.get("createdfor"),
                               company_id=request.POST.get("companyid_job"),
                               reference_id=request.POST.get("reference_id"),
                               job_type=request.POST.get("job_type"),
                               parent_company_id=request.user.company_id,
                               created_by_id=request.user.id,
                               company_identifier=c_name[:3] + '-',
                               job_seq=Job.objects.filter(company_id=com_id).count() + 1,
                               location=request.POST.get("location"),

                                    )

             jobs.save()
        else:
             jobs = Job.objects.create(job_description=request.POST.get("jobdescription"),
                                      job_title=request.POST.get("jobtitle"),
                                      primary_skills=request.POST.get("primaryskills"),
                                      lead_time=request.POST.get("leadtime"),
                                      experience=request.POST.get("experience"),
                                      no_positions=request.POST.get("positions"),
                                      created_for=request.POST.get("createdfor"),
                                      company_id=request.POST.get("companyid_job"),
                                      reference_id=request.POST.get("reference_id"),
                                      job_type=request.POST.get("job_type"),
                                      parent_company_id=request.user.company_id,
                                      created_by_id=request.user.id,
                                      company_identifier=c_name[:3] + '-',
                                      job_seq=Job.objects.filter(company_id=com_id).count() + 1,
                                      location=request.POST.get("location"),
                                      job_end_date=date1,

                                      )

             jobs.save()

        skills = Skill.objects.all().values_list("skill")
        skill_set = [skill[0] for skill in skills]
        skils_count= Skill.objects.all().count()+1
        print(skils_count)


        print(skill_set, "vvvvvvvvvvvvvvvvvvvvvvccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc")
        add_skils = [skil for skil in primary_skills if skil not in skill_set]
        for add_skill in add_skils:

            Skill.objects.create(id=skils_count,skill = add_skill)
            skils_count=skils_count+1

        print(add_skils, "aaaaaaaaaaaaaaaasssssssssssssddddddddddddddddddddddddffffffffffffffffffffffff")
        comp=Company.objects.filter(id=com_id).values_list('company_name').first()
        print(comp[0],"**********************")
        comp1=comp[0]
        users=User.objects.filter(company__id=com_id).values_list('first_name').first()
        user1=users[0]
        print(users[0],"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")



        send_mail_job(email_list,jobs,comp1,user1)
        data={"msg" : get_message(6)}
        #
        # c_id = request.POST.get("companyid")
        return JsonResponse(data,safe=False)


operatorcreatejob = OperatorsJob.as_view()

@method_decorator(csrf_exempt, name='dispatch')
class ProfileList(LoginRequiredMixin, View):


    def post(self, request, *args, **kwargs):
        print(request.POST)
        profile_id = request.POST.get('pro_id')
        availability=request.POST.get("availability")
        print(availability,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(profile_id,"****************")
        jjj=JobProfileAssociation.objects.filter(resume=profile_id).filter(receive_update_dt__gte = date.today()).update(candidate_name=request.POST['candidate_name'],candidate_email=request.POST['candidate_email'], primary_skills=request.POST['primary_skills'],phone_number=request.POST['phone_number'],experience= request.POST['experience'],current_ctc=request.POST['current_ctc'],current_role=request.POST.get("currentrole"),current_company = request.POST['current_company'],expected_ctc = request.POST['expected_ctc'] , location = request.POST['location'] ,notice_period = request.POST['notice_period'])
        print(jjj , "only one in this caseeeeeeeeeeeeeeeeeeeeeeee")
        try:
            profiles = Profile.objects.get(id=profile_id)
            print(profiles,"$$$$$$$$$$$$$$$$$$$$$$$")
            profiles.candidate_name = request.POST['candidate_name']
            profiles.candidate_email = request.POST['candidate_email']
            profiles.phone_number = request.POST['phone_number']
            profiles.primary_skills = request.POST['primary_skills']
            print(request.POST.get('primary_skills'))
            profiles.current_company = request.POST['current_company']

            profiles.experience = request.POST['experience']
            profiles.current_ctc = request.POST['current_ctc']
            profiles.expected_ctc = request.POST['expected_ctc']
            profiles.notice_period = request.POST['notice_period']
            profiles.location = request.POST['location']
            profiles.availability=request.POST['availability']

            profiles.current_role = request.POST['currentrole']

            profiles.alternate_phone_number = request.POST['alter_ph_num']
            print("aftwer location")

            profiles.is_interviewer = request.POST['is_interviewr']
            profiles.interview_skills = request.POST['interviewr_skills']
            profiles.save()

            print("aftwer location")

            # profiles.save()
            print("inside profile")
            data={"msg": get_message(7)}
            return JsonResponse(data,safe=False)

        except Exception as e:

            print(e , "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc")
            data={"msg":get_message(8)}
            return JsonResponse(data, safe=False)


        return JsonResponse({"msg": get_message(7)}, safe=False)

updateprofile = ProfileList.as_view()


class Updatecustomer(LoginRequiredMixin, View):
    def get(self, request, user_id=None, *args, **kwargs):
        if user_id is None:
            return User.objects.all()

        else:

            User.objects.get(id=user_id)

        return render(request, "customerlist.html")

    def post(self, request, *args, **kwargs):
        print(request.POST, "pppppppppppppppppppp")
        user_id = request.POST.get('User_id', "llllllllllll")
        print(id)
        try:

            customers = User.objects.get(id=user_id)
            customers.first_name = request.POST['first_name']
            customers.phone_number = request.POST['phone_number']

            customers.email = request.POST['email']
            print("vjxhCAG")

            customers.save()

            print(customers.__dict__)
        except:
            import sys
            print(str(sys.exc_info()), "dddddddddddddddd")
        print(request.path_info)
        return HttpResponseRedirect(reverse("operatorpage"))


updatecust = Updatecustomer.as_view()


class Updateoper(LoginRequiredMixin, View):
    def get(self, request, user_id=None, *args, **kwargs):
        if user_id is None:
            return User.objects.all()

        else:

            User.objects.get(id=user_id)

        return render(request, "Operatorlist.html")

    def post(self, request, *args, **kwargs):
        print(request.POST, "intervvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
        user_id = request.POST.get('User_id')
        company_id = request.POST.get("Company_id")
        print(request.POST.get("interview_service"))
        if request.POST.get("interview_service") == "on":
            print("here")
            interview_service = True
        else:
            interview_service = False
        try:



            operators = User.objects.get(id=user_id)
            company = Company.objects.get(id=company_id)


            operators.first_name = request.POST['first_name']
            operators.last_name = request.POST['last_name']
            operators.phone_number = request.POST['phone_number']

            operators.email = request.POST['email']
            company.interview_services = interview_service
            print("vjxhCAG")
            company.save()

            operators.save()
            # companies.save()

            print(operators.__dict__)
        except Exception as e:
            print(e)
            import sys
            print(str(sys.exc_info()), "dddddddddddddddd")
        print(request.path_info)
        return HttpResponseRedirect(reverse("operatorlist"))


updateoperator = Updateoper.as_view()


# for display already attached profiles when operator login

@method_decorator(csrf_exempt, name='dispatch')
class ProfileDetails(LoginRequiredMixin, View):
    def get(self, request):
        # search_val = request.GET.get("profiles")
        # print(search_val, "this is search value ")
        # if search_val is None:
        profiles = JobProfileAssociation.objects.filter(job_id=request.GET.get('jobid')).values(
            'resume__candidate_email', 'resume__candidate_name', 'resume__phone_number', 'resume__current_company',
            'resume__primary_skills', 'resume__experience', 'resume__current_ctc', 'resume__expected_ctc',
            'resume__notice_period', 'resume__resume_name','final_status', 'job_id', 'id')
        print(profiles, "this is p detils")
        data = {"profiledetails": list(profiles)}
        return JsonResponse(data, safe=False)


profiledetails = ProfileDetails.as_view()


# for updating status of the candidate
@method_decorator(csrf_exempt, name='dispatch')
class StatusUpdate(View):
    def post(self, request):
        print(request.POST, "this is comming data")

        jpa = JobProfileAssociation.objects.filter(id=request.POST.get("job_id")).update(
            final_status=request.POST.get("status"))


        data = {"msg":get_message(9)}
        return JsonResponse(data, safe=False)
from jobs.models import Status
import shutil, os
from smartrec.settings import BASE_DIR
from django.conf import settings
import errno


def get_status(self):
    print("aaaaaaaaaaaaa")
    next_level_status = Status.objects.filter(level__contains=[2]).values_list("status", flat=True)
    return list(next_level_status)

def send_email_attach_profile(subject,email_message,to_email_list,user_email):
    print(user_email,"^^^^^^^^^^^^^^^")
    from_string = '{0} <{1}>'.format("aaaaaaaaaaaaaaaaaaa", user_email)
    email = EmailMessage(subject,email_message,user_email,to=to_email_list)

    email.send()

# for attaching profiles
@method_decorator(csrf_exempt, name='dispatch')
class AttachProfile(LoginRequiredMixin, View):
    def covert_object(self,obj):
        obj['updated_on']=datetime.date.strftime(obj['updated_on'], "%m/%d/%Y")
        return obj
    def get(self, request):
        print("helooooooooooooooooo")
        jobid = request.GET.get('jobid')
        comid = request.GET.get('comid')

        profiles = JobProfileAssociation.objects.filter(job_id=jobid).values_list('candidate_email', flat=True)

        profile = Profile.objects.filter(added_for_id=request.user.company_id, latest=True).exclude(
            candidate_email__in=list(profiles)).exclude(
            Q(candidate_name="") and Q(primary_skills="") and Q(experience="") and Q(
                notice_period="")).values('id', 'candidate_email', 'phone_number',
                                                                 'percent_rise', 'current_company', 'candidate_name',
                                                                 'notice_period', 'experience', 'primary_skills',
                                                                 'resume_name', 'expected_ctc', 'current_ctc',"availability" , "current_role" ,
                                                                    "updated_on")

        profile= [self.covert_object(x) for x in profile]
        data = {"data": list(profile), "jobid": jobid, "comid": comid, "x": "False"}

        return JsonResponse(data, safe=False)


    def post(self, request):
        import json
        global fp
        data = json.loads(request.body)
        print(".....................................................................................>>>>>>>>>>")
        company_name = request.user.company.company_name
        company_id = data['comid']
        job_id = data['jobid']
        print(data['comid'],"...............................................")
        allresumes = []
        user_details = User.objects.filter(company_id = data['comid']).values_list("first_name" , "email").first()
        usermail  =[ user_details[1] ]
        username = user_details[0]
        customer_company_name = Company.objects.filter(id=data['comid']).values_list('company_name').first()

        folder =  company_name + '/'+ str(customer_company_name[0])
        print(data['profile_ids'],"sssssdddddddddddddddddffffffffffffffffffffeeeeeeeeeeeeeee")
        job_details = Job.objects.filter(id = job_id).values_list("job_title").first()
        print(job_details[0])
        job_title = str(job_details[0])
        for profile_ids in data['profile_ids']:
            print(profile_ids)
            f=Profile.objects.filter(id=profile_ids).values_list('resume_name','candidate_name','candidate_email','phone_number',
                                                                 'primary_skills','experience','current_ctc',
                                                                 'expected_ctc','current_company','notice_period',
                                                                 'location','extracted_words', "current_role","resume_path").first()
            Profile.objects.filter(id=profile_ids).update(attached=True)
            sendfiles = "media/" + f[13]
            allresumes.append(sendfiles)

            files = settings.MEDIA_ROOT + "/" + company_name + "/" + str(f[0])
            print(files , "this is file.......")
            dest = settings.MEDIA_ROOT + "/" + folder + "/" + str(f[0])
            print(dest , "this is where to save")
            dest1 = settings.MEDIA_ROOT + "/" + folder + "/"
            status_id = Status.objects.filter(status = "Shared").values_list("id").first()
            # print(data['comid'] , '******************************************')
            resume = JobProfileAssociation.objects.filter(resume=profile_ids,company_id =company_id,job_id=job_id).count()
            print(resume, "1111111111111111111")
            print(type(resume))
            if resume  > 0 :
                data = {"msg" : get_message(10)}
                return JsonResponse(data , safe=False)

            else :
                try:

                    try:
                        print("inside tryyyyyyyyyyyyyyyy")
                        shutil.copy(files, dest)
                        print("outside tryyyyyyyyyyyyy")
                    except:
                        print("inside catch,...........")

                        os.makedirs(os.path.dirname(dest1))
                        shutil.copy(files, dest)
                    jpa=JobProfileAssociation.objects.create(job_id=job_id,
                                                         resume=profile_ids,
                                                         company_id=company_id,
                                                         created_by_id=request.user.id,
                                                         updated_by_id=request.user.id,
                                                         status_id=status_id[0],
                                                         associated_profile_path = folder+"/"+str(f[0]),
                                                         candidate_name=f[1],
                                                         candidate_email=f[2],
                                                         phone_number=f[3],
                                                         primary_skills=f[4],
                                                         experience=f[5],
                                                         current_ctc=f[6],
                                                         expected_ctc=f[7],
                                                         current_company=f[8],
                                                         notice_period=f[9],
                                                         location=f[10],
                                                         extracted_words=f[11],
                                                         current_role = f[12],
                                                         vc_id_id=request.user.company.id,
                                                         vc_name=request.user.company.company_name,
                                                         cc_name=customer_company_name[0],
                                                         receive_update_dt=date.today() + timedelta(45))


                    jpa.save()

                    job_id =job_id
                    com_id = company_id
                    data = {"job_id": job_id, "com_id": com_id, "msg": get_message(14)}


                    print(job_id , com_id, "aaaaaaaaaaaaaaaaaa")


                    EMAIL_USE_TLS = True
                    EMAIL_HOST = 'smtp.gmail.com'
                    EMAIL_PORT = 587
                    subject = "New Profiles Attached for Job - "+ job_title
                    email_message = "Dear"+ " "+   username +",\n\nWe have shared new profiles for the Job - "+ job_title +".\nPlease click here  to login to forsta to see the profiles. \n\nIf you have any challenges in accessing, please reach out to your contact.\nThank you \n Forsta Admin \nforsta.in "


                    # email_list = ["suresh.kori@aqua-cap.com"]
                    print(usermail)
                    email_list =usermail

                        # excel_file = ["media/" + p[0] for p in resume]

                    try:
                        mail = imaplib.IMAP4_SSL(EMAIL_HOST)

                        mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                    except Exception:
                        pass
                    send_email_attach_profile(subject, email_message, email_list,  EMAIL_HOST_USER)
                    data = {"msg": get_message(19)}
                    return JsonResponse(data, safe=False)






                except:
                    data = {"msg" : get_message(13)}
        return JsonResponse(data , safe=False)


attachprofiles = AttachProfile.as_view()


# for creating conversation database
@method_decorator(csrf_exempt, name='dispatch')
class Conversations(View):
    def post(self, request):
        print(request.POST.get('jpa_id'), "jpa id id is ...........................")
        jpa_id = request.POST.get('jpa_id')
        if request.user.is_operator :
            JobProfileAssociation.objects.filter(id=jpa_id).update(msg_read_status = 2)
        else :
            JobProfileAssociation.objects.filter(id=jpa_id).update(msg_read_status = 1)

        if request.POST.get('company_id') is None:
            print(request.user.company.parent_company_id, "am coming here...................................")
            a = request.user.company.parent_company_id

        else:
            a = request.POST.get('company_id')

        data_msg = [{"msg" : request.POST.get('chat'),"msg_from" : request.user.company.id , "msg_to" : a, "user" : request.user.short_name}]
        datatoappend = {"msg" : request.POST.get('chat'),"msg_from" : request.user.company.id , "msg_to" : a,"user" : request.user.short_name}
        print(data_msg ,"asssssssssssssssssssssssssssssssss")
        jpa_id = Conversation.objects.filter(jpa_id=jpa_id).first()
        if hasattr(jpa_id, "jpa_id"):
            print("inside hereeeeeeeeeeeeeeeeeeeeeeeee")
            chat=Conversation.objects.filter(jpa_id=request.POST.get('jpa_id')).values("conversation_to")
            print(chat[0] , "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print(chat[0]['conversation_to'])
            lst=chat[0]['conversation_to']
            lst.append(datatoappend)
            print(lst)
            chat=Conversation.objects.filter(jpa_id=request.POST.get('jpa_id')).update(conversation_to =lst )

            print("upend here")
        else:
            Conversation.objects.create(jpa_id=request.POST.get('jpa_id'),conversation_to=data_msg,initiated_by_id=request.user.id)
        # now = datetime.datetime.now()
        # print(request.POST.get('jobid'), "this is job id.............................")
        # j_id = request.POST.get('jobid')
        # print(request.POST.get('jpa_id'), "jpa id id is ...........................")
        # print(request.user.short_name)
        # print(request.POST.get('chat'))
        # print(request.POST.get('company_id'), 'this is none here........................................')
        #
        # if request.POST.get('company_id') is None:
        #     print(request.user.company.parent_company_id, "am coming here...................................")
        #     a = request.user.company.parent_company_id
        #
        # else:
        #     a = request.POST.get('company_id')
        #
        # Conversation.objects.create(conversation_to=request.POST.get('chat'),
        #                             job_id=request.POST.get('jobid'),
        #                             jpa_id=request.POST.get('jpa_id'),
        #                             conversation_on=now.strftime("%d-%B"),
        #                             initiated_by_id=request.user.id,
        #                             created_by_id=request.user.id,
        #                             updated_by_id=request.user.id,
        #                             send_to_id=a
        #                             )

        pro_conversation = Conversation.objects.filter(jpa_id=request.POST.get("jpa_id")).values('conversation_to').order_by(
                    'created_dt')

        # def get_conversation():
        #     p_id = Conversation.objects.filter(jpa_id=request.POST.get("jpa_id")).values('conversation_to').order_by(
        #         'created_dt')
        #     for p in p_id:
        #         print(p)
        # def check_send(id):
        #     if id is request.user.id:
        #         print(id, request.user.id, 'thsi should equl.......................')
        #         return True
        #     else:
        #         print("coming here.............cccccccccccccccccccc.")
        #         return False
        #
        # data = [{"con": get_conversation()}]
        print(list(pro_conversation), "this is conversatios list after creating/.,...............................................")
        data = {"msg" : pro_conversation[0]['conversation_to']}

        return JsonResponse(data, safe=False)


# for display to alreay send messages...........
class ConversationDisplay(View):
    def get(self, request):
        user_id = request.user.id
        jpa_id = request.GET.get("jpaid")
        print(jpa_id)
        jpa_id = Conversation.objects.filter(jpa_id=jpa_id).first()
        JobProfileAssociation.objects.filter(id= request.GET.get("jpaid")).update(msg_read_status=0)

        if hasattr(jpa_id, "jpa_id"):
            pro_conversation = Conversation.objects.filter(jpa_id=request.GET.get("jpaid")).values('conversation_to')

            def check_send(id):
                return True if id is request.user.id else False
            data = [{"msg" : msgs['msg'], "send_by" : check_send(msgs['msg_from'])} for msgs in  pro_conversation[0]['conversation_to'] ]
        else :
            data={}
        return JsonResponse(data, safe=False)


# for deleting the operator when admin log in
class DeleteOperator(View):
    def get(self, request):
        print("i will delete")
        print(request.GET.get('op_id'))
        print(request.GET.get('comid'))
        comid = request.GET.get('comid')
        opid = request.GET.get('op_id')

        opr = User.objects.get(id=opid)
        cus = Company.objects.get(id=comid)

        print(opr)
        cus.delete()
        opr.delete()
        return HttpResponseRedirect(reverse("operatorlist"))


# for checking the existing mail........

@method_decorator(csrf_exempt, name='dispatch')
class CheckMail(View):
    def post(self, request):
        print("working.....................")
        status = True

        email = User.objects.filter(email=request.POST.get("email")).first()
        print(email)

        mail = request.POST.get("email")
        print(mail)
        if hasattr(email, "email"):
            status = False
        else:
            status = True

        print(status)
        return HttpResponse(json.dumps({"status": status}))


#When operator logs in and he can see his company operators
class OperatorDetails(View) :
    def get(self,request):
        detail=User.objects.filter(company_id = request.user.company.id)
        print(detail, "list of company operators")
        context = {"details" : detail}
        return render(request,"operatorsdetails.html",context)



from django.template import Context

@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(user_permission, name='dispatch')
# @method_decorator(is_operator, name='dispatch')
# @method_decorator(is_company, name='dispatch')
class ResetPassword(View):

    def email_two(request,email,ctx):
        subject = "RESET PASSWORD"
        to = email
        from_email = base.EMAIL_HOST
        message = render_to_string(base.BASE_DIR+'/template/emailtemplate.html', ctx)
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()



    def post(self,request,*args,**kwargs):
        email=request.POST.get('email')
        print(email,"^^^^^^^^^^^^^^^")
        host=request.get_host()
        print(host,"&&&&&&&&&&&&")
        if request.is_secure():
            protocol = 'https://forsta.in'
        else:
            protocol = 'http://forsta.in'
        if User.objects.filter(email=email).exists():
            key_url = generate_secretkey(email)
            ctx={"validation_link":protocol+'/resetpassword/?token='+key_url}
            print(ctx)
            self.email_two([email],ctx)
            data={"msg":get_message(15)}
        else:
            data={"msg":get_message(16)}

        return JsonResponse(data, safe=False)

    def get(self,request,*args,**kwargs):
        token = request.GET.get("token")
        email=authenticate_key(token)
        print(token, "ssssssssssss" ,)


        return render(request,'confirm.html',{"email":email})


@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(user_permission, name='dispatch')
# @method_decorator(is_operator, name='dispatch')
# @method_decorator(is_company, name='dispatch')
class ChangePassword(View):

    def post(self,request,*args,**kwargs):
        token = request.POST.get("token")
        print(token,"^^^^^^^^^^^^")
        email = authenticate_key(token)
        print(email,"$$$$$$$$$$$$$$$$$")
        new_password=request.POST.get("new_password")
        print(new_password,"&&&&&&&&&&&&&&")
        confirm_password=request.POST.get("confirm_password")
        print(confirm_password,"***********")
        data={}
        if email is not None and new_password is not None and confirm_password is not None:
            if User.objects.filter(email=email).exists():
                if new_password == confirm_password:
                    print("True")
                    user=User.objects.filter(email=email).first()
                    user.set_password(new_password)
                    user.save()
                    data={"msg":get_message(18),"success":True}


                else:
                    print("False")
                    data = {"msg": get_message(17), "success": False}

        return JsonResponse(data,safe=False)


def html_to_excel_view(request) :

    operators = User.objects.filter(is_operator=True)
    print(operators)
    raw_data = [{"Company Name": o.company.company_name,"Contact Name": o.first_name,"Email Id" : o.email , "Contact Number" : o.phone_number,"No Of Clients":o.get_total_company_count()} for o in operators]
    df = pd.DataFrame(raw_data, columns=['Company Name', 'Contact Name' , 'Email Id' , 'Contact Number' , 'No Of Clients'])
    print(df, "this is table")
    filename = 'operatorlist.xlsx'
    file_path=base.MEDIA_ROOT +'/'+ filename
    writer = pd.ExcelWriter(file_path,engine='xlsxwriter')
    df.to_excel(writer, sheet_name='sheet1',index=False)
    writer.save()
    print(file_path)
    # response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # response['Content-Disposition'] = 'attachment; filename = operatorlist.xls'
    # response.write(df)
    data={"fname":filename}
    # data={"path":file_path}
    # return JsonResponse(data,safe=False)
    return JsonResponse(data,safe=False)
    # if os.path.exists('/home/aveto/Downloads/operatorlist.xlsx' % id):


    # raw_data={
    #         "Name" : ['a','s','d','f','q','w'],
    #         "Company Name" :['q','w','q','w','w','d']
    #

    # return HttpResponseRedirect(reverse('operatorlist'))

def html_to_excel_view_email(request) :

    operators = User.objects.filter(is_operator=True)
    print(operators)
    raw_data = [{"Company Name": o.company.company_name,"Contact Name": o.first_name,"Email Id" : o.email , "Contact Number" : o.phone_number,"No Of Clients":o.get_total_company_count()} for o in operators]
    df = pd.DataFrame(raw_data, columns=['Company Name', 'Contact Name' , 'Email Id' , 'Contact Number' , 'No Of Clients'])
    print(df, "this is table")

    writer = pd.ExcelWriter('operatorlist.xlsx')

    df.to_excel(writer,'sheet1',index=False)
    writer.save()

    data={"msg":"success"}

    return JsonResponse(data,safe=False)




class OperatorListToExcle(View):
    def get(self,request):
        print("aaaaaaaaaaaaaaaaaacccccccccccccccccccrrrrrrrrrrrrrrrrrrrrrssssssssssssssssss")
        # company = Company.objects.filter(parent_company_id=request.user.company_id).values_list("id", flat=True)






        # customers = User.objects.filter(company_id__in=list(company))
        company_list = Company.objects.filter(parent_company_id=request.user.company_id).values_list("id", flat=True)
        customers_list = User.objects.filter(company_id__in=list(company_list))

        raw_data = [{"Company Name": o.company.company_name, "Contact Name": o.first_name, "Email Id": o.email,
                     "Contact Number": o.phone_number} for o in customers_list]
        df = pd.DataFrame(raw_data,
                          columns=['Company Name', 'Contact Name', 'Email Id', 'Contact Number'])
        print(df, "this is table")
        filename = 'Customerlist.xlsx'
        file_path = base.MEDIA_ROOT + '/' + filename
        writer = pd.ExcelWriter(file_path,engine='xlsxwriter')
        df.to_excel(writer, sheet_name='sheet1',index=False)
        writer.save()
        data={"fname":filename}

        return JsonResponse(data,safe=False)


class ProfileListToExcle(View):
    def get(self,request):
        profiles_list = Profile.objects.filter(added_for_id=request.user.company_id, latest=True)
        raw_data = [{"Name": o.candidate_name, "Email": o.candidate_email, "Phone": o.phone_number,
                     "Primary Skill": o.primary_skills, "Current Company": o.current_company, "Total Experience": o.experience, "CTC": o.current_ctc, "Expected CTC": o.expected_ctc, "Notice Period": o.notice_period} for o in profiles_list]
        df = pd.DataFrame(raw_data,
                          columns=['Name', 'Email', 'Phone', 'Primary Skill', 'Currenct Company', 'Total Experience', 'CTC', 'Expected CTC', 'Notice Period'])
        print(df, "this is table")
        filename = 'Profilerepositorylist.xlsx'
        file_path = base.MEDIA_ROOT + '/' + filename
        writer = pd.ExcelWriter(file_path,engine='xlsxwriter')
        df.to_excel(writer, sheet_name='sheet1',index=False)
        writer.save()
        data = {"fname": filename}

        return JsonResponse(data,safe=False)


class JpaListToExcle(View):
    def get(self,request):
        print(request.GET)

        job_id=request.GET.get('job_id')
        print(request.GET.get('job_id'),"**************")

        def get_date(self, date):
            # obj['created_dt'] = datetime.date.strftime(obj['created_dt'], "%m/%d/%Y")
            if date is None:
                return None
                print(date , "this  is date")
            else:
                return datetime.date.strftime(date, "%m/%d/%Y")

        job_status = request.GET.get("status_id")
        company_id = request.GET.get("company_id")
        if company_id is "0" and job_status is "0" :
                jpalist = Job.objects.filter(
                    (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__isnull=False)) & (Q(
                        parent_company_id=request.user.company.id) | Q(JobProfileAssociation_job__vc_id_id=request.user.company.id))).values_list(                                                                                                   "JobProfileAssociation_job__created_dt",

                                                                                "company__company_name",
                                                                                "job_title",
                                                                                "reference_id",
                                                                                "JobProfileAssociation_job__candidate_name",
                                                                                "JobProfileAssociation_job__candidate_email",
                                                                                "JobProfileAssociation_job__phone_number",

                                                                                "JobProfileAssociation_job__primary_skills",
                                                                                "JobProfileAssociation_job__current_company",
                                                                                "JobProfileAssociation_job__experience",
                                                                                 "JobProfileAssociation_job__location",
                                                                                "JobProfileAssociation_job__current_ctc",
                                                                                "JobProfileAssociation_job__expected_ctc",
                                                                                "JobProfileAssociation_job__notice_period",
                                                                                "JobProfileAssociation_job__final_status",)

        elif company_id != "0" and job_id is "0"  and job_status is "0" :

            jpalist = Job.objects.filter(
                (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__company_id=company_id)) & (
                        Q(company_id=company_id) | Q(JobProfileAssociation_job__company_id=company_id))).values_list(
                                                                                "JobProfileAssociation_job__created_dt",

                                                                                "company__company_name",
                                                                                "job_title",
                                                                                "reference_id",
                                                                                "JobProfileAssociation_job__candidate_name",
                                                                                "JobProfileAssociation_job__candidate_email",
                                                                                "JobProfileAssociation_job__phone_number",

                                                                                "JobProfileAssociation_job__primary_skills",
                                                                                "JobProfileAssociation_job__current_company",
                                                                                "JobProfileAssociation_job__experience",
                                                                                 "JobProfileAssociation_job__location",
                                                                                "JobProfileAssociation_job__current_ctc",
                                                                                "JobProfileAssociation_job__expected_ctc",
                                                                                "JobProfileAssociation_job__notice_period",
                                                                                "JobProfileAssociation_job__final_status",)
        elif company_id != "0" and job_id != "0":
            jpalist = Job.objects.filter(
            (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__isnull=False)) & (Q(
                JobProfileAssociation_job__job_id=job_id) & Q(JobProfileAssociation_job__company_id=company_id) | Q(id=job_id))).values_list(
                                                                                "JobProfileAssociation_job__created_dt",

                                                                                "company__company_name",
                                                                                "job_title",
                                                                                "reference_id",
                                                                                "JobProfileAssociation_job__candidate_name",
                                                                                "JobProfileAssociation_job__candidate_email",
                                                                                "JobProfileAssociation_job__phone_number",

                                                                                "JobProfileAssociation_job__primary_skills",
                                                                                "JobProfileAssociation_job__current_company",
                                                                                "JobProfileAssociation_job__experience",
                                                                                 "JobProfileAssociation_job__location",
                                                                                "JobProfileAssociation_job__current_ctc",
                                                                                "JobProfileAssociation_job__expected_ctc",
                                                                                "JobProfileAssociation_job__notice_period",
                                                                                "JobProfileAssociation_job__final_status",)

        elif company_id is "0" and job_status != "0":

            jpalist = Job.objects.filter(
                (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__isnull=False)) & (Q(
                    parent_company_id=request.user.company.id) | Q(
                    JobProfileAssociation_job__vc_id_id=request.user.company.id)) & Q(
                    job_status_value=job_status)).values_list("JobProfileAssociation_job__created_dt",

                                                                                "company__company_name",
                                                                                "job_title",
                                                                                "reference_id",
                                                                                "JobProfileAssociation_job__candidate_name",
                                                                                "JobProfileAssociation_job__candidate_email",
                                                                                "JobProfileAssociation_job__phone_number",

                                                                                "JobProfileAssociation_job__primary_skills",
                                                                                "JobProfileAssociation_job__current_company",
                                                                                "JobProfileAssociation_job__experience",
                                                                                 "JobProfileAssociation_job__location",
                                                                                "JobProfileAssociation_job__current_ctc",
                                                                                "JobProfileAssociation_job__expected_ctc",
                                                                                "JobProfileAssociation_job__notice_period",
                                                                                "JobProfileAssociation_job__final_status",)


        elif company_id != '0' and job_status != '0':
            print("inside hereeeeeeeeeeeeeee")

            jpalist = Job.objects.filter(
                (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__isnull=False)) & ((Q(
                    company_id=company_id) | Q(JobProfileAssociation_job__company_id=company_id)) & Q(
                    job_status_value=job_status))).values_list("JobProfileAssociation_job__created_dt",

                                                                                "company__company_name",
                                                                                "job_title",
                                                                                "reference_id",
                                                                                "JobProfileAssociation_job__candidate_name",
                                                                                "JobProfileAssociation_job__candidate_email",
                                                                                "JobProfileAssociation_job__phone_number",

                                                                                "JobProfileAssociation_job__primary_skills",
                                                                                "JobProfileAssociation_job__current_company",
                                                                                "JobProfileAssociation_job__experience",
                                                                                 "JobProfileAssociation_job__location",
                                                                                "JobProfileAssociation_job__current_ctc",
                                                                                "JobProfileAssociation_job__expected_ctc",
                                                                                "JobProfileAssociation_job__notice_period",
                                                                                "JobProfileAssociation_job__final_status",)



        print(jpalist ,"ssssssssssssuuuuuuuuuuuuu")
        raw_data = [{"Date" :  get_date(self,p[0]), "Company": p[1],"Job Title": p[2], "Reference Id" : p[3] , "Candidate Name": p[4], "Candidate Email": p[5], "Candidate Phone": p[6],"Skills": p[7], "Current Company":p[8], "Years Of Exp": p[9],"Current Location": p[10], "CTC": p[11], "Expected CTC":p[12], "Notice Period":p[13],"Current Status" : p[14]} for p in jpalist]
        df = pd.DataFrame(raw_data,
                            columns = ['Date', 'Company','Job Title','Reference','Candidate Name', 'Candidate Email', 'Candidate Phone', 'Skills', 'Current Company','Years Of Exp', 'CTC', 'Expected CTC', 'Notice Period','Current Status'])

            # job_title=JobProfileAssociation.objects.filter(job_id=job_id).values_list("job__job_title").first()
            # print(job_title,"$$$$$$$$$$$$$$$$$")
            # res=job_title[0]
            # print(job_title[0],"*******************8")
        print(df, "this is table")
            # filename = 'Profiles for '+res +".xlsx"
        filename = 'dashboardlist_vendor.xlsx'
        file_path = base.MEDIA_ROOT + '/' + filename
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='sheet1', index=False)
        writer.save()

        data = {"fname": filename,"msg": "success"}
        return JsonResponse(data,safe=False)


class Dashboard_to_excel(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_operator:
            print("coming here")
            dashboarddetails = JobProfileAssociation.objects.filter(vc_id_id=request.user.company.id).values_list("cc_name",
                                                                                                             "job__job_seq",
                                                                                                             "job__job_title",
                                                                                                             "job__no_positions",
                                                                                                             "candidate_name",
                                                                                                             "phone_number",
                                                                                                             "final_status")
            raw_data = [{"Company": p[0], "Job ID": p[1], "Job Title": p[2], "No Positions": p[3],
                         "Candidate Name": p[4], "Phone Number": p[5], "Status": p[6]
                         } for p in dashboarddetails]

            df = pd.DataFrame(raw_data,
                              columns=['Company', 'Job ID', 'Job Title', 'No Positions', 'Candidate Name',
                                       'Phone Number',
                                       'Status'])
            filename = 'dashboardlist_vendor.xlsx'
            file_path = base.MEDIA_ROOT + '/' + filename
            writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='sheet1', index=False)
            writer.save()
            data = {"fname": filename}

            return JsonResponse(data, safe=False)

        elif request.user.is_company:
            dashboarddetails = JobProfileAssociation.objects.filter(company_id=request.user.company.id).values_list(
                "cc_name",
                "job__job_seq",
                "job__job_title",
                "job__no_positions",
                "candidate_name",
                "phone_number",
                "final_status")
            raw_data = [{"Company": p[0], "Job ID": p[1], "Job Title": p[2], "No Positions": p[3],
                         "Candidate Name": p[4], "Phone Number": p[5], "Status": p[6]
                         } for p in dashboarddetails]

            df = pd.DataFrame(raw_data,
                              columns=['Company', 'Job ID', 'Job Title', 'No Positions', 'Candidate Name',
                                       'Phone Number',
                                       'Status'])
            filename = 'dashboardlist_customer.xlsx'
            file_path = base.MEDIA_ROOT + '/' + filename
            writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='sheet1', index=False)
            writer.save()
            data = {"fname": filename}

            return JsonResponse(data, safe=False)

class Userlist_to_excel(View):
    def get(self,request,*args,**kwargs):
        users=User.objects.filter(company_id=request.user.company.id)
        print(users,"************8")
        raw_data = []
        # company_data=[]
        for p in users:
            company={"Company Name":p.company.company_name,"Customer/Operator Name": p.first_name, "Email": p.email, "Phone Number": p.phone_number,"No of clients":Company.objects.filter(created_by_id = p.id).count()}
            raw_data.append(company)
        df = pd.DataFrame(raw_data,
                          columns=['Company Name', 'Customer/Operator Name', 'Email', 'Phone Number', 'No of clients',
                                   ])
        filename = 'userlist.xlsx'
        file_path = base.MEDIA_ROOT + '/' + filename
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='sheet1', index=False)
        writer.save()
        data = {"fname": filename}

        return JsonResponse(data, safe=False)


class CustomerJobList_to_excel(View):
    def get(self,request,*args,**kwargs):
        jobid=request.GET.get('jobid')
        print(jobid,"************8")
        profiles=JobProfileAssociation.objects.filter(job_id=jobid).values_list('candidate_name','primary_skills', 'current_company',
                 'experience', 'current_ctc',
                'expected_ctc', 'notice_period', 'final_status'
                )
        raw_data = [{"Candidate Name": p[0], "Primary Skills": p[1], "Current Company": p[2], "Experience": p[3],
                     "CTC": p[4], "Expected CTC": p[5], "Notice Period": p[6], "Status": p[7],
                    } for p in profiles]
        df = pd.DataFrame(raw_data,
                          columns=['Candidate Name', 'Primary Skills', 'Current Company', 'CTC','Experience', 'Expected CTC', 'Notice Period',
                                   'Status',
                                   ])
        filename = 'customerjoblist.xlsx'
        file_path = base.MEDIA_ROOT + '/' + filename
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='sheet1', index=False)
        writer.save()
        data = {"fname": filename}
        return JsonResponse(data, safe=False)



from django.db.models import Count
class JobProfileAssociationDelete(View):
    def get(self,request,*args,**kwargs):
        print(request.GET.get("jpa_id"),"__________-----")
        print(request.GET.get("job_id"))
        jpa_id=request.GET.get("jpa_id")
        jobdel = JobProfileAssociation.objects.filter(id=jpa_id)

        associated_profile_path=JobProfileAssociation.objects.filter(id=request.GET.get("jpa_id")).values_list("company_id",'associated_profile_path').first()
        print(str(associated_profile_path[0]), "length of profilessssssssssssssss")
        count_of_associated_path=JobProfileAssociation.objects.filter(Q(company_id=str(associated_profile_path[0]))& Q(associated_profile_path=str(associated_profile_path[1]))).count()
        print(count_of_associated_path, "count")

        if count_of_associated_path is 1 :
            remove_assocoated_profile=settings.MEDIA_ROOT +'/' +str(associated_profile_path[1])
            print(remove_assocoated_profile , "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

            os.remove(remove_assocoated_profile)

        jobdel.delete()

        data={"msg":get_message(11), "job_id":request.GET.get("job_id")}


        return JsonResponse(data,safe=False)





class DeleteProfiles(View):

    def get(self, request):
        print("i will delete")
        print(request.GET.get('p_id'),"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        profileid = request.GET.get('p_id')
        jpa_id = JobProfileAssociation.objects.filter(resume_id = profileid).first()
        print(jpa_id,"ataches")
        if hasattr(jpa_id , "resume_id"):
            data = {"msg": "This profile cannot be deleted as it is attached to a job"}
            return JsonResponse(data, safe=False)
        else :
            data={"msg" : "delete"}
            return JsonResponse(data, safe=False)

class DeleteUnAttachedProfile(View):
    def get(self,request):
        profileid = request.GET.get('p_id')
        print(profileid)
        profile_id = Profile.objects.get(id=profileid)
        profile_path=Profile.objects.filter(id=profileid).values_list("resume_path").first()

        remove_profile = settings.MEDIA_ROOT + '/' + str(profile_path[0])
        os.remove(remove_profile)
        profile_id.delete()
        data = {"msg": get_message(11)}
        return JsonResponse(data, safe=False)
        # return HttpResponseRedirect(reverse('operatorpage'))

        # cus = Company.objects.get(id=comid)

        # print(opr)
        # cus.delete()
        # opr.delete()


class DownloadProfile(View) :
    def get(self, request):
        profileid = request.GET.get('p_id')
        print(profileid)
        profile_id = Profile.objects.get(id=profileid)
        profile_path = Profile.objects.filter(id=profileid).values_list("resume_path").first()
        filename=str(profile_path[0])
        data = {"filename" : filename}
        return JsonResponse(data , safe=False)

import re
def change_date_format(dt):
        return  re.sub(r'(\d{1,2})-(\d{1,2})-(\d{4})', r'\3-\2-\1',dt)


from smartrec.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage
def send_email(subject,email_message,to_email_list,excel_file,user_email):
    print(user_email,"^^^^^^^^^^^^^^^")
    from_string = '{0} <{1}>'.format("aaaaaaaaaaaaaaaaaaa", user_email)
    print(from_string,"###########3333333")
    email = EmailMessage(subject,email_message,user_email,to=to_email_list)
    for file in excel_file:
        try :
            email.attach_file(file)
        except :
            pass
    email.send()

# def send_mail_job(to_email_list,job_list):
def send_mail_job(to_email_list,raw_data,data1,data2):

    subject="Job details"
    # details="Dear Vendor," \
    #         "please work on the following details:"
    # email=EmailMessage(subject,EMAIL_HOST_USER,to=to_email_list)
    # email.attach_file(excel)
    # email.send()
    from_email = base.EMAIL_HOST
    # job_list={"job__list":raw_data}
    # print(job_list[0],"*****************88888888888888888")
    # print(raw_data.job_title,"***********************")
    data={"raw_data":raw_data,"data1":data1,"data2":data2}
    print(data1[0],"##########################33")
    print(data2,"@@@@@@@@@@@@@@@@@@@@@@@@")
    message = render_to_string(base.BASE_DIR + '/template/job_detail.html',data)
    msg = EmailMessage(subject,message, to=to_email_list, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()


import smtplib
import imaplib
import email
import os
from django.core.mail.message import EmailMessage

class Sendmail_withAxcel(View):
    def get(self,request):
        print()
        print("Excel attached")
        job_id = request.GET.get('job_id')
        company_id=request.GET.get('company_id')
        print(company_id , "it should comeeeeeeeeeeeeeee")
        job_status=request.GET.get('status_id')
        user_email=request.user.email
        password=request.GET.get("Mail_pass")
        EMAIL_USE_TLS = True
        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_PORT = 587
        EMAIL_HOST_USER = user_email
        EMAIL_HOST_PASSWORD = password
        subject=request.GET.get("subjects")
        email_message = request.GET.get("details")
        email_list=[request.GET.get("mail_id")]
        # excel_file=request.GET.get("excelsheet")+'.xlsx'
        # excel_file="example.ics"
        # excel_file="media/dashboardlist_vendor.xlsx"
        # excel_file = ["media/ibm/Abhay Agarawal_38_9_15_lSAdGUQ.doc","media/dashboardlist_vendor.xlsx"]

        if company_id != "0" and job_id != "0" :
            resume = JobProfileAssociation.objects.filter(job_id = job_id).values_list("associated_profile_path")
            print(resume)
            excel_file = ["media/"+p[0] for p in resume]
        excel_file.append("media/dashboardlist_vendor.xlsx")
        print(type(excel_file))
        print(excel_file , "fffffffffffiiiiiiiiiiiiiiillllllllllllleeeeeeeeeee nnnnnnnnnnaaaaaaaaaammmmmmmmmmmmmmeeeeeeeeee")

        try:
            mail = imaplib.IMAP4_SSL(EMAIL_HOST)

            mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        except Exception:
            pass
        send_email(subject, email_message,email_list, excel_file,EMAIL_HOST_USER)
        data={"msg" : get_message(19)}
        return JsonResponse(data , safe=False)



class Attach_excel_to_mail(View):
    def get(self,request):
        abc=request.GET.get('excelsheet')
        print(abc , "sssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
        print(type(abc), "............................................................>>>>>>>>>>>>>>>>>>>>>>")
        if abc == 'customerlist' :
            print("operlist")
            company_list = Company.objects.filter(parent_company_id=request.user.company_id).values_list("id",
                                                                                                         flat=True)
            customers_list = User.objects.filter(company_id__in=list(company_list))

            raw_data = [{"Company Name": o.company.company_name, "Contact Name": o.first_name, "Email Id": o.email,
                         "Contact Number": o.phone_number} for o in customers_list]
            df = pd.DataFrame(raw_data,
                              columns=['Company Name', 'Contact Name', 'Email Id', 'Contact Number'])
            filename = 'customerlist.xlsx'

            writer = pd.ExcelWriter('customerlist.xlsx')

            df.to_excel(writer, 'sheet1', index=False)
            writer.save()
            data = {"msg": "success","filename":filename}

            return JsonResponse(data, safe=False)

        elif abc == 'profilelist_excel' :
            print("profile...........................................................................................................")
            profiles_list = Profile.objects.filter(added_for_id=request.user.company_id, latest=True)
            raw_data = [{"Name": o.candidate_name, "Email": o.candidate_email, "Phone": o.phone_number,
                         "Primary Skill": o.primary_skills, "Current Company": o.current_company,
                         "Total Experience": o.experience, "CTC": o.current_ctc, "Expected CTC": o.expected_ctc,
                         "Notice Period": o.notice_period} for o in profiles_list]
            df = pd.DataFrame(raw_data,
                              columns=['Name', 'Email', 'Phone', 'Primary Skill', 'Currenct Company',
                                       'Total Experience', 'CTC', 'Expected CTC', 'Notice Period'])
            print(df, "this is table")
            filename = 'profilelist_excel.xlsx'
            writer = pd.ExcelWriter('profilelist_excel.xlsx')

            df.to_excel(writer, 'sheet1', index=False)
            writer.save()
            data = {"msg": "success","filename":filename}

            return JsonResponse(data, safe=False)
        elif abc == 'jpalist':
            job_id = request.GET.get('jobid')
            print(request.GET.get('jobid'), "**************")
            jpalist = JobProfileAssociation.objects.filter(job_id=request.GET.get('jobid')).values_list(
                'job__job_title',
                'resume__candidate_email', 'resume__candidate_name', 'resume__phone_number', 'resume__current_company',
                'resume__primary_skills', 'resume__resume_path', 'resume__experience', 'resume__current_ctc',
                'resume__expected_ctc', 'resume__notice_period', 'resume__resume_name', 'final_status', 'job_id',
                'resume_id')
            print(jpalist, "ssssssssssssuuuuuuuuuuuuu")
            raw_data = [{"Job Title": p[0], "Name": p[2], "Email": p[1], "Phone": p[3],
                         "Primary Skill": p[5], "Current Company": p[4], "Total Experience": p[7], "CTC": p[8],
                         "Expected CTC": p[9], "Notice Period": p[10], "status": p[12]} for p in jpalist]
            df = pd.DataFrame(raw_data,
                              columns=['Job Title', 'Name', 'Email', 'Phone', 'Primary Skill', 'Current Company',
                                       'Total Experience', 'CTC',
                                       'Expected CTC', 'Notice Period', 'status'])

            print(df, "this is table")
            filename = 'jpalist.xlsx'
            writer = pd.ExcelWriter('jpalist.xlsx')

            df.to_excel(writer, 'sheet1', index=False)
            writer.save()
            data = {"filename":filename}
            return JsonResponse(data, safe=False)

        elif abc == 'dashboardlist_vendor':
                print("hi,'''''''''''''")
                dashboarddetails = JobProfileAssociation.objects.filter(vc_id_id=request.user.company.id).values_list("cc_name",
                                                                                                    "job__job_seq",
                                                                                                    "job__job_title",
                                                                                                    "job__no_positions",
                                                                                                    "candidate_name",
                                                                                                    "phone_number",
                                                                                                    "final_status")
                raw_data = [{"Company": p[0], "Job ID": p[1], "Job Title": p[2], "No Positions": p[3],
                             "Candidate Name": p[4], "Phone Number": p[5], "Status": p[6]
                            } for p in dashboarddetails]

                df = pd.DataFrame(raw_data,
                                  columns=['Company', 'Job ID', 'Job Title', 'No Positions', 'Candidate Name', 'Phone Number',
                                            'Status'])
                filename = 'dashboardlist_vendor.xlsx'
                writer = pd.ExcelWriter('dashboardlist_vendor.xlsx')
                df.to_excel(writer, 'sheet1', index=False)
                writer.save()
                data = {"filename": filename}
                return JsonResponse(data, safe=False)

        elif abc == 'dashboardlist_customer':
                print(request.user.company.id,"###########")
                dashboarddetails = JobProfileAssociation.objects.filter(company_id=request.user.company.id).values_list(
                    "cc_name",
                    "job__job_seq",
                    "job__job_title",
                    "job__no_positions",
                    "candidate_name",
                    "phone_number",
                    "final_status")
                print(dashboarddetails,"*************")
                raw_data = [{"Company": p[0], "Job ID": p[1], "Job Title": p[2], "No Positions": p[3],
                             "Candidate Name": p[4], "Phone Number": p[5], "Status": p[6]
                             } for p in dashboarddetails]

                df = pd.DataFrame(raw_data,
                                  columns=['Company', 'Job ID', 'Job Title', 'No Positions', 'Candidate Name',
                                           'Phone Number',
                                           'Status'])
                filename = 'dashboardlist_customer.xlsx'
                writer = pd.ExcelWriter('dashboardlist_customer.xlsx')
                df.to_excel(writer, 'sheet1', index=False)
                writer.save()
                data = {"filename": filename}
                print(data,"(((((((((((")
                return JsonResponse(data, safe=False)

        elif abc == 'userlist':
            print(request.user.company.id)
            print(request.user.company.company_name)
            users = User.objects.filter(company_id=request.user.company.id)
            print(users, "************8")
            raw_data = []
            # company_data=[]
            for p in users:
                company = {"Company Name": p.company.company_name, "Customer/Operator Name": p.first_name,
                           "Email": p.email, "Phone Number": p.phone_number,
                           "No of clients": Company.objects.filter(created_by_id=p.id).count()}
                raw_data.append(company)
            df = pd.DataFrame(raw_data,
                              columns=['Company Name', 'Customer/Operator Name', 'Email', 'Phone Number',
                                       'No of clients',
                                       ])
            filename = 'userlist.xlsx'
            writer = pd.ExcelWriter('userlist.xlsx')
            df.to_excel(writer, 'sheet1', index=False)
            writer.save()
            data = {"filename": filename}
            return JsonResponse(data, safe=False)

        elif abc == 'customerjoblist':
            jobid = request.GET.get('jobid')
            print(jobid, "************8")
            profiles = JobProfileAssociation.objects.filter(job_id=jobid).values_list('candidate_name',
                                                                                      'primary_skills',
                                                                                      'current_company',
                                                                                      'experience', 'current_ctc',
                                                                                      'expected_ctc', 'notice_period',
                                                                                      'final_status'
                                                                                      )
            raw_data = [{"Candidate Name": p[0], "Primary Skills": p[1], "Current Company": p[2], "Experience": p[3],
                         "CTC": p[4], "Expected CTC": p[5], "Notice Period": p[6], "Status": p[7],
                         } for p in profiles]
            df = pd.DataFrame(raw_data,
                              columns=['Candidate Name', 'Primary Skills', 'Current Company', 'CTC', 'Experience',
                                       'Expected CTC', 'Notice Period',
                                       'Status',
                                       ])
            filename = 'customerjoblist.xlsx'
            writer = pd.ExcelWriter('customerjoblist.xlsx')
            df.to_excel(writer, 'sheet1', index=False)
            writer.save()
            data = {"filename": filename}
            return JsonResponse(data, safe=False)

            return JsonResponse(data, safe=False)


class DeleteJob(View):
    def get(self,request,*args,**kwargs):
        jobid=request.GET.get('job_id')
        print(jobid)
        jobs=Job.objects.filter(id=jobid)
        jobs.delete()

        data={"msg": get_message(11)}

        return JsonResponse(data,safe=False)




from django_datatables_view.base_datatable_view import BaseDatatableView


@method_decorator(csrf_exempt, name='dispatch')

class UpdateJob(View):
    def post(self,request,*args,**kwargs):
        job_id = request.POST.get('job_id')
        print(request.POST.get('job_type'),"$$$$$$$$$$$$44")
        print(job_id, "aaaaaaaaaaaaaaaaaa")
        job_end = request.POST.get('job_end_date')
        y=change_date_format(job_end)
        print(y)

        try:
            print("ssssssssssssssssssssssssssssssss")
            jobs = Job.objects.get(id=job_id)
            print(jobs)
            print(request.POST)
            print(request.POST['primary_skills'])
            jobs.job_description = request.POST['job_description']
            jobs.primary_skills = request.POST['primary_skills']
            jobs.lead_time = request.POST['lead_time']
            jobs.experience = request.POST['experience']
            jobs.no_positions = request.POST['no_positions']
            jobs.created_for = request.POST['created_for']
            jobs.reference_id = request.POST['reference_id']
            jobs.job_type = request.POST['job_type']
            jobs.location=request.POST['location']
            jobs.job_end_date=y
            jobs.job_status_value=request.POST['job_status']


            jobs.save()
            data={"msg":get_message(7)}
            return JsonResponse(data, safe=False)
        except Exception:
            print("cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc")
            return JsonResponse({"msg":get_message(8)}, safe=False)

        return JsonResponse({"msg": get_message(7)}, safe=False)

class JobDetailsShow(View) :
    def get(self,request):
        print(request.GET.get("job_id"),"**************")
        jobs = Job.objects.filter(id=request.GET.get("job_id"))
        jobs1=Job.objects.filter(id=request.GET.get("job_id")).values_list('job_end_date').first()
        import re

        def change_date_format(dt):
            return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)

        dt1 = change_date_format(str(jobs1[0]))
        l=[]
        for p in jobs:
            job_details={'job_description':p.job_description,"job_title":p.job_title,"primary_skills":p.primary_skills,
                         'lead_time':p.lead_time,"experience":p.experience,"created_for":p.created_for,"reference_id":p.reference_id,
                         "no_positions":p.no_positions,"location":p.location,"job_end_date":dt1,"job_id":p.id,"job_type":p.job_type, "job_status": p.job_status_value}
            l.append(job_details)
        data = {'jobs':l}

        return JsonResponse(data , safe=False)

import re
class ProfileRepositoryLoad(BaseDatatableView):
    model = Profile
    # columns = ['Name', 'Email', 'Phone', 'primary_skills', 'Current company','Experience', 'Ctc',
    #            'Excepted-ctc','notice_period', ]
    columns = ['candidate_name','A','candidate_email','phone_number' , "Role",'primary_skills','current_company','experience','current_ctc','expected_ctc','notice_period','updated_on','resume_name']
    # order_columns = ['candidate_name','candidate_email','phone_number' 'primary_skills', 'current_company','experience','current_ctc','expected_ctc','notice_period']

    def get_initial_queryset(self):
        print(self.request.user.company_id)
        print("nice job venky................................................................................................")
        qs = Profile.objects.filter(added_for_id=self.request.user.company_id, latest=True).order_by('-updated_on')
        print(qs, "this is qs_list of profile ref 1234...................")


        return qs

    def filter_queryset(self, qs):
        # use request parameters to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        job_id = self.request.GET.get('job_id')

        print(search)
        if search:
            qs = qs.filter(Q(candidate_email__icontains=search) | Q(candidate_name__icontains=search) | Q(phone_number__icontains=search)| Q(primary_skills__icontains=search)| Q(current_company__icontains=search)| Q(experience__icontains=search)| Q(current_ctc__icontains=search)| Q(expected_ctc__icontains=search)| Q(notice_period__icontains=search) | Q(updated_on__icontains=search)| Q(current_role__icontains=search))

        return qs

    def render_column(self, row, column):
        pro=Profile.objects.filter(id=row.id).values_list('resume_name',"updated_on").first()
        extension=str(pro[0])
        ll = str(pro[1]).split(" ")
        DD = datetime.timedelta(days=14)
        ll1 = str(datetime.datetime.now() - DD).split(" ")
        if column == 'candidate_name':
            return ("{0}").format('<td value="'+row.candidate_name+'">'+row.candidate_name+'</td>')
        if column == 'candidate_email' :
            return ("{0}").format('<td>'+row.candidate_email+'</td>')
        if column == 'phone_number' :
            return ("{0}").format(row.phone_number)
        if column == 'Role':
            return ("{0}").format(row.current_role)
        if column == 'primary_skills' :
            return ("{0}").format(row.primary_skills)
        if column == 'current_company':
            return ("{0}").format(row.current_company)
        if column == 'experience' :
                return ("{0}").format(row.experience)
        if column == 'current_ctc' :
                return ("{0}").format(row.current_ctc)
        if column == 'expected_ctc' :
                return ("{0}").format(row.expected_ctc)
        if column == 'notice_period' :
                return ("{0}").format(row.notice_period)
        if column == 'updated_on':

            return ("{1}").format('DD MM YYYY',row.updated_on.date())
        if column == 'resume_name':

            return '{0}'.format(
                '<td value="' + str(
                    row.resume_path) + '"><img  src="../static/css/document-edit-icon.png" width="22px" class="editbtn changeprofile" aria-hidden="true" id="' + str(
                    row.resume_path) + '" value=' + str(
                    row.id) + ' title="View & Edit Profile"></img> <i onclick="delete_profile(' + str(
                    row.id) + ')" class="fa fa-trash-o fa-3x icon_large"title="Delete Profile"></i><a href="../media/'+str(row.resume_path)+'" download class="fa fa-download icon_small"title="Download Profile"></a></td>')

        if column == 'A':
            if str(row.availability) == "yes":
                return '{0}'.format('<td ><i id="' + str(row.availability) + '" class="dot"></i></td>')

# <a href="test.txt" download>Click here</a>

class ProfileDetailsShow(View):
    def get(self,request):
        p_id = request.GET.get("p_id")
        profile_objects =Profile.objects.all().values_list('id', flat=True)
        profile_details= Profile.objects.filter(id=p_id).values('id', 'candidate_email', 'phone_number',
                                                                 'percent_rise', 'current_company', 'candidate_name',
                                                                 'notice_period', 'experience','current_role', 'primary_skills',
                                                                 'resume_path', 'expected_ctc', 'current_ctc', 'location','resume_name','availability' ,'notes' ,                                                                                   'interview_skills','is_interviewer',"alternate_phone_number", "updated_on")
        print(profile_objects)
        data ={"details" : list(profile_details)}
        return JsonResponse(data , safe=False)


class ProfileAttachCheck(View) :
    def get(self, request):
        print("i will delete")
        print(request.GET.get('job_id'), "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        job_id=request.GET.get('job_id')
        jpa_id = JobProfileAssociation.objects.filter(job_id=job_id).first()
        print(jpa_id, "ataches")
        if hasattr(jpa_id, "job_id"):
            data = {"msg": "This job cannot be deleted as it contains profiles"}
            return JsonResponse(data, safe=False)
        else:

            data = {"msg": get_message(11)}
            return JsonResponse(data, safe=False)

from jobs.models import Skill
class GetAllSkills(View):
    def get(self,request):
        skills= Skill.objects.all().values("skill")
        data = {"skills": list(skills) }
        print(data ,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.........................................")
        return JsonResponse(data , safe=False)


class GetDashboardDetails(View):
    def get(self,request):
        if request.user.is_operator :

            vender_cid= request.GET.get("c_id")

            job_deta = []
            job_status_value = request.GET.get("job_status_value")
            job_status =  request.GET.get("status_value")
            print(job_status , "this is job status")
            job_id = request.GET.get("j_id")
            print(type(job_id))
            print(job_id , " job id jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")

            j_idlist = JobProfileAssociation.objects.filter(company_id=vender_cid).values_list("job_id",
                                                                                               flat=True)


            print(vender_cid , "companyid cccccccccccccccccccccccccccccccccccccccccccccc")


            #         dashboarddetails123 = Job.objects.filter(parent_company_id=request.user.company.id).exclude(
        #             id__in=list(j_idlist)).values_list("job_title", "job_seq", "company__company_name", "no_positions",
        #                                                "id")
        #         for x in dashboarddetails123:
        #                 y = (x + empty_str)
        #                 job_deta.append(y)
        #
        #
            if vender_cid == '0' and  job_id == '0' and job_status is None:
                print("coming hereeeeeeeeeeeeeeeee.....................")

                dashboarddetails = Job.objects.filter(
                    (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__isnull=False)) & (Q(
                        parent_company_id=request.user.company.id) | Q(JobProfileAssociation_job__vc_id_id=request.user.company.id))).values_list("job_title",

                                                                                "job_seq",
                                                                                "JobProfileAssociation_job__cc_name",
                                                                                "no_positions",
                                                                                "JobProfileAssociation_job__candidate_name",
                                                                                "JobProfileAssociation_job__candidate_email",
                                                                                "JobProfileAssociation_job__phone_number",
                                                                                "company_id",
                                                                                "JobProfileAssociation_job__current_role" ,
                                                                                "JobProfileAssociation_job__primary_skills",
                                                                                "JobProfileAssociation_job__current_company",
                                                                                "JobProfileAssociation_job__experience",
                                                                                "JobProfileAssociation_job__current_ctc",
                                                                                "JobProfileAssociation_job__expected_ctc",
                                                                                "JobProfileAssociation_job__notice_period",
                                                                                "JobProfileAssociation_job__associated_profile_path",
                                                                                "JobProfileAssociation_job__final_status",

                                                                                "id",
                                                                                "JobProfileAssociation_job__id",
                                                                                "company__company_name" ,
                                                                                "JobProfileAssociation_job__msg_read_status"  )
                print(dashboarddetails.query, "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
                print(list(dashboarddetails), "this is listtttttttttttttttttttttttt")


            elif vender_cid is '0' and job_id is '2':
                print("inside hereeeeeeeeeeeeeee")

                dashboarddetails = Job.objects.filter(
                    (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__isnull=False)) & (Q(
                        parent_company_id=request.user.company.id)| Q(
                        JobProfileAssociation_job__vc_id_id=request.user.company.id)) & Q(job_status_value=job_status)).values_list("job_title",

                                                                                                   "job_seq",
                                                                                                   "JobProfileAssociation_job__cc_name",
                                                                                                   "no_positions",
                                                                                                   "JobProfileAssociation_job__candidate_name",
                                                                                                   "JobProfileAssociation_job__candidate_email",
                                                                                                   "JobProfileAssociation_job__phone_number",
                                                                                                   "company_id",
                                                                                                   "JobProfileAssociation_job__current_role",
                                                                                                   "JobProfileAssociation_job__primary_skills",
                                                                                                   "JobProfileAssociation_job__current_company",
                                                                                                   "JobProfileAssociation_job__experience",
                                                                                                   "JobProfileAssociation_job__current_ctc",
                                                                                                   "JobProfileAssociation_job__expected_ctc",
                                                                                                   "JobProfileAssociation_job__notice_period",
                                                                                                   "JobProfileAssociation_job__associated_profile_path",
                                                                                                   "JobProfileAssociation_job__final_status",

                                                                                                   "id",
                                                                                                   "JobProfileAssociation_job__id",
                                                                                                   "company__company_name",
                                                                                                   "JobProfileAssociation_job__msg_read_status")
            elif vender_cid != '0' and job_id is '2':
                print("inside hereeeeeeeeeeeeeee")

                dashboarddetails = Job.objects.filter(
                    (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__isnull=False)) & ((Q(
                        company_id=vender_cid) | Q(JobProfileAssociation_job__company_id=vender_cid)) &   Q(
                        job_status_value=job_status))).values_list("job_title",

                                                                                                   "job_seq",
                                                                                                   "JobProfileAssociation_job__cc_name",
                                                                                                   "no_positions",
                                                                                                   "JobProfileAssociation_job__candidate_name",
                                                                                                   "JobProfileAssociation_job__candidate_email",
                                                                                                   "JobProfileAssociation_job__phone_number",
                                                                                                   "company_id",
                                                                                                   "JobProfileAssociation_job__current_role",
                                                                                                   "JobProfileAssociation_job__primary_skills",
                                                                                                   "JobProfileAssociation_job__current_company",
                                                                                                   "JobProfileAssociation_job__experience",
                                                                                                   "JobProfileAssociation_job__current_ctc",
                                                                                                   "JobProfileAssociation_job__expected_ctc",
                                                                                                   "JobProfileAssociation_job__notice_period",
                                                                                                   "JobProfileAssociation_job__associated_profile_path",
                                                                                                   "JobProfileAssociation_job__final_status",

                                                                                                   "id",
                                                                                                   "JobProfileAssociation_job__id",
                                                                                                   "company__company_name",
                                                                                                   "JobProfileAssociation_job__msg_read_status")
            elif vender_cid != '0' and job_id is '2' and job_status != None :
                print("inside hereeeeeeeeeeeeeee")

                dashboarddetails = Job.objects.filter(
                    (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__isnull=False)) & (Q(
                        company_id=vender_cid) & Q(job_status_value=job_status) | Q(
                        JobProfileAssociation_job__company_id=vender_cid))).values_list("job_title",

                                                                                        "job_seq",
                                                                                        "JobProfileAssociation_job__cc_name",
                                                                                        "no_positions",
                                                                                        "JobProfileAssociation_job__candidate_name",
                                                                                        "JobProfileAssociation_job__candidate_email",
                                                                                        "JobProfileAssociation_job__phone_number",
                                                                                        "company_id",
                                                                                        "JobProfileAssociation_job__current_role",
                                                                                        "JobProfileAssociation_job__primary_skills",
                                                                                        "JobProfileAssociation_job__current_company",
                                                                                        "JobProfileAssociation_job__experience",
                                                                                        "JobProfileAssociation_job__current_ctc",
                                                                                        "JobProfileAssociation_job__expected_ctc",
                                                                                        "JobProfileAssociation_job__notice_period",
                                                                                        "JobProfileAssociation_job__associated_profile_path",
                                                                                        "JobProfileAssociation_job__final_status",

                                                                                        "id",
                                                                                        "JobProfileAssociation_job__id",
                                                                                        "company__company_name",
                                                                                        "JobProfileAssociation_job__msg_read_status")



            elif vender_cid != '0' and request.GET.get("j_id") == '0' :

                dashboarddetails = Job.objects.filter(
                    (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__company_id=vender_cid)) &(
                        Q(company_id=vender_cid) | Q(JobProfileAssociation_job__company_id=vender_cid) )).values_list("job_title",

                                                                                "job_seq",
                                                                                "JobProfileAssociation_job__cc_name",
                                                                                "no_positions",
                                                                                "JobProfileAssociation_job__candidate_name",
                                                                                "JobProfileAssociation_job__candidate_email",
                                                                                "JobProfileAssociation_job__phone_number",
                                                                                "company_id",
                                                                                "JobProfileAssociation_job__current_role" ,
                                                                                "JobProfileAssociation_job__primary_skills",
                                                                                "JobProfileAssociation_job__current_company",
                                                                                "JobProfileAssociation_job__experience",
                                                                                "JobProfileAssociation_job__current_ctc",
                                                                                "JobProfileAssociation_job__expected_ctc",
                                                                                "JobProfileAssociation_job__notice_period",
                                                                                "JobProfileAssociation_job__associated_profile_path",
                                                                                "JobProfileAssociation_job__final_status",

                                                                                "id",
                                                                                "JobProfileAssociation_job__id",
                                                                                "company__company_name" ,
                                                                                "JobProfileAssociation_job__msg_read_status"  )






            elif vender_cid != '0' and request.GET.get("j_id") != '0' :


                # dashboarddetails = JobProfileAssociation.objects.filter(company_id=vender_cid,job_id=job_id).values_list("job__job_title","job__job_seq", "cc_name", "job__no_positions" , "candidate_name", "candidate_email", "phone_number", "company_id", "current_role","primary_skills","current_company","experience","current_ctc","expected_ctc","notice_period", "associated_profile_path","final_status", "job__id","id", "company__company_name", "msg_read_status").order_by("-updated_on")
                dashboarddetails = Job.objects.filter(
                    (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__isnull=False) ) & (Q(
                        JobProfileAssociation_job__job_id=job_id) & Q(
                        JobProfileAssociation_job__company_id=vender_cid) | Q(id=job_id))).values_list("job_title",

                                                                                                   "job_seq",
                                                                                                   "JobProfileAssociation_job__cc_name",
                                                                                                   "no_positions",
                                                                                                   "JobProfileAssociation_job__candidate_name",
                                                                                                   "JobProfileAssociation_job__candidate_email",
                                                                                                   "JobProfileAssociation_job__phone_number",
                                                                                                   "company_id",
                                                                                                   "JobProfileAssociation_job__current_role",
                                                                                                   "JobProfileAssociation_job__primary_skills",
                                                                                                   "JobProfileAssociation_job__current_company",
                                                                                                   "JobProfileAssociation_job__experience",
                                                                                                   "JobProfileAssociation_job__current_ctc",
                                                                                                   "JobProfileAssociation_job__expected_ctc",
                                                                                                   "JobProfileAssociation_job__notice_period",
                                                                                                   "JobProfileAssociation_job__associated_profile_path",
                                                                                                   "JobProfileAssociation_job__final_status",

                                                                                                   "id",
                                                                                                   "JobProfileAssociation_job__id",
                                                                                                   "company__company_name",
                                                                                                   "JobProfileAssociation_job__msg_read_status")




            elif vender_cid is '0' and job_id != '0' :
                print("both is not none hereeeee")
                dashboarddetails = JobProfileAssociation.objects.filter(vc_id_id=request.user.company.id , job_id=job_id).values_list("job__job_title","job__job_seq", "cc_name", "job__no_positions" , "candidate_name", "candidate_email", "phone_number", "company_id", "current_role","primary_skills","current_company","experience","current_ctc","expected_ctc","notice_period", "associated_profile_path","final_status", "job__id","id", "company__company_name", "msg_read_status").order_by("-updated_on")
            elif vender_cid is '2' and job_id is '2':
                 print("inside hereeeeeeeeeeeeeee")

                 dashboarddetails = Job.objects.filter(
                    (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__isnull=False)) & (Q(
                        parent_company_id=request.user.company.id) & Q(job_status_value=job_status) | Q(JobProfileAssociation_job__vc_id_id=request.user.company.id))).values_list("job_title",

                                                                                "job_seq",
                                                                                "JobProfileAssociation_job__cc_name",
                                                                                "no_positions",
                                                                                "JobProfileAssociation_job__candidate_name",
                                                                                "JobProfileAssociation_job__candidate_email",
                                                                                "JobProfileAssociation_job__phone_number",
                                                                                "company_id",
                                                                                "JobProfileAssociation_job__current_role" ,
                                                                                "JobProfileAssociation_job__primary_skills",
                                                                                "JobProfileAssociation_job__current_company",
                                                                                "JobProfileAssociation_job__experience",
                                                                                "JobProfileAssociation_job__current_ctc",
                                                                                "JobProfileAssociation_job__expected_ctc",
                                                                                "JobProfileAssociation_job__notice_period",
                                                                                "JobProfileAssociation_job__associated_profile_path",
                                                                                "JobProfileAssociation_job__final_status",

                                                                                "id",
                                                                                "JobProfileAssociation_job__id",
                                                                                "company__company_name" ,
                                                                                "JobProfileAssociation_job__msg_read_status"  )

        else :
            print("he is customer")

            vender_cid = request.GET.get("c_id")

            print(vender_cid ,"ccccccccccccccccccccccccccccccccccccc")
            job_id = request.GET.get("j_id")
            print(type(job_id))
            print(job_id, " job id jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
            if job_id is '0':
                dashboarddetails = Job.objects.filter(
                    (Q(JobProfileAssociation_job__isnull=True) | Q(JobProfileAssociation_job__isnull=False)) & (Q(
                        company_id=request.user.company.id) | Q(
                        JobProfileAssociation_job__company_id=request.user.company.id))).values_list("job_title",

                                                                                "job_seq",
                                                                                "JobProfileAssociation_job__cc_name",
                                                                                "no_positions",
                                                                                "JobProfileAssociation_job__candidate_name",
                                                                                "JobProfileAssociation_job__candidate_email",
                                                                                "JobProfileAssociation_job__phone_number",
                                                                                "company_id",
                                                                                "JobProfileAssociation_job__current_role" ,
                                                                                "JobProfileAssociation_job__primary_skills",
                                                                                "JobProfileAssociation_job__current_company",
                                                                                "JobProfileAssociation_job__experience",
                                                                                "JobProfileAssociation_job__current_ctc",
                                                                                "JobProfileAssociation_job__expected_ctc",
                                                                                "JobProfileAssociation_job__notice_period",
                                                                                "JobProfileAssociation_job__associated_profile_path",
                                                                                "JobProfileAssociation_job__final_status",

                                                                                "id",
                                                                                "JobProfileAssociation_job__id",
                                                                                "company__company_name" ,
                                                                                "JobProfileAssociation_job__msg_read_status",
                                                                                "JobProfileAssociation_job__customer_checked"                     )
            else :
                dashboarddetails = JobProfileAssociation.objects.filter(job_id=job_id).values_list("job__job_title","job__job_seq", "cc_name", "job__no_positions" , "candidate_name", "candidate_email", "phone_number", "company_id", "current_role","primary_skills","current_company","experience","current_ctc","expected_ctc","notice_period", "associated_profile_path","final_status", "job__id","id", "company__company_name", "msg_read_status").order_by("-updated_on")

        # dashboarddetails = list(chain(job_deta, dashboarddetails))
        print(list(dashboarddetails) , "superrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")

        data = { "dashboarddetails" : list(dashboarddetails)}
        return  JsonResponse(data , safe=False)


class GetDashboardDetails_job(View):
    def get(self,request):

        vender_cid= request.user.company.id

        dashboarddetails = []
        print(vender_cid , "cccccccccccccccccccccccccccccccccccccccccccccc")
        j_idlist=JobProfileAssociation.objects.filter(vc_id_id =vender_cid).values("job_id",flat=True)
        job_table_details = Job.objects.filter(parent_company_id=request.user.company.id).exclude(id__in=list(j_idlist))
        print(job_table_details , "chanlage................... big..........................")
        if request.user.is_operator:

            dashboarddetails = JobProfileAssociation.objects.filter(vc_id_id =vender_cid).values_list("cc_name","job__job_seq", "job__job_title", "job__no_positions" , "candidate_name", "phone_number", "final_status","updated_on" ).order_by("-updated_on")
        else :
            dashboarddetails = JobProfileAssociation.objects.filter(company_id=vender_cid).values("cc_name", "job__job_seq",
                                                                                                "job__job_title",
                                                                                                "job__no_positions",
                                                                                                "candidate_name",
                                                                                                  "phone_number",
                                                                                                "final_status",
                                                                                                  "customer_checked").order_by("-updated_on")



            # for p in comp:
            #     details=JobProfileAssociation.objects,filter(company_id=p[0]).values("cc_name", "job__job_seq",
            #                                                                                     "job__job_title",
            #                                                                                     "job__no_positions",
            #                                                                                     "candidate_name",
            #                                                                                       "phone_number",
            #                                                                                     "final_status",
            #                                                                                       "customer_checked").order_by("-updated_on")
            #     print(details,"******44444-----------")

        # data={"data" : {"com_name" : dashboarddetails[0],"job_id" : dashboarddetails[1],"job_tittle" : dashboarddetails[2],"positions" : dashboarddetails[3],"can_name" : dashboarddetails[4],"status" :dashboarddetails[5]}}
        print(list(dashboarddetails), "##############")
        print(list(details),"###@@@@@###$$$$$$$$$$$")
        data = { "dashboarddetails" : list(dashboarddetails),"details":list(details)}
        return  JsonResponse(data , safe=False)

        # dashboarddetails.append(d_details.value)
        print(dashboarddetails,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # print(list(d_details) , "asaasaasasasasaasaasasasasasasasassasasas")
        data = { "dashboarddetails" : list(dashboarddetails)}
        return  JsonResponse(data , safe=False)


class GetAllJobs(View) :
    def get(self,request):
        if request.user.is_operator :
            all_job=Job.objects.filter(parent_company_id = request.user.company.id).values("id","job_title")
            all_company = Company.objects.filter(parent_company_id= request.user.company.id).values("id","company_name")
            print(all_job , "aaaaaaaaaaaaaaa")
        else:
            all_job=Job.objects.filter(company_id = request.user.company.id).values("id","job_title")
            all_company = []

        data = {"jobs" : list(all_job) , "companies" : list(all_company)}
        return  JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CreateNotes(View) :
    def get(self,request):

        resume_id = request.GET.get("resume_id")
        print(resume_id)
        pr_id = Profile.objects.filter(id=resume_id).first()
        if hasattr(pr_id, "id"):
            notes = Profile.objects.filter(id=resume_id).values("notes")

        else:
            notes = JobProfileAssociation.objects.filter(id=resume_id).values("notes")
        data = {"notes" : list(notes)}
        return JsonResponse(data, safe=False)


    def post(self,request):
        resume_id = request.POST.get("resume_id")
        print(resume_id)
        pr_id = Profile.objects.filter(id=resume_id).first()
        if hasattr(pr_id, "id"):
            Profile.objects.filter(id=resume_id).update(notes = request.POST.get("notes"))


        else:
            JobProfileAssociation.objects.filter(id=resume_id).update(notes = request.POST.get("notes"))
        data = {"msg" : get_message(12)}
        return JsonResponse(data , safe=False)


class AllJobStatus(View):
    def get(self,request):
        status = Status.objects.filter(status_value=2).values("status" , "id")
        data = {"status" : list(status)}
        return JsonResponse(data , safe=False)

# To update and disable and enable myusers in operator page
@method_decorator(csrf_exempt, name='dispatch')
class MyUserUpdate(View) :
    def post(self,request):
        print(request.POST , "*****************")

        user = User.objects.filter(id = request.POST.get('user_id')).update(first_name = request.POST.get("first_name"),email = request.POST.get("email"),phone_number =  request.POST.get("phone_number"),is_active = request.POST.get('user_status'))
        return JsonResponse({"msg" : get_message(7)} , safe=False)


class CheckPrimaryUser(View):
    def get(self,request):
        print(request.GET.get("user_id"))
        id=request.user.id
        user = User.objects.filter(id = request.user.id).values("primary_user")
        user_active = User.objects.filter(id = request.GET.get("user_id")).values("is_active")
        data = {"user" : list(user) , "user_active" : list(user_active) , "user_id" : id}
        return JsonResponse(data ,safe=False)





class Customerchecked(View) :
    def get(self,request):
        print("coming.....................pa")
        jpa_id = request.GET.get("jpa_id")
        jpa_table = JobProfileAssociation.objects.filter(id = jpa_id).update(customer_checked = True)
        data ={}
        return JsonResponse(data , safe=False)

















