from django.views import View
from nltk import RegexpTokenizer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
from io import BytesIO as StringIO
import datetime
import textract
import os
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# import spacy
# import en_core_web_sm
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from smartrec.settings import BASE_DIR
from profiles.models import Profile
from company.models import Company
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
# nltk.download()
import time

# class Extraction(View):
#     global now
#     now = datetime.datetime.now()
#     # converts pdf, returns its text content as a string
#     def pdf(pdffile, pages=None, ):
#         print(int(round(time.time() * 1000)), "beggning time")
#
#         if not pages:
#             pagenums = set()
#         else:
#             pagenums = set(pages)
#
#         output = StringIO()
#         manager = PDFResourceManager()
#         converter = TextConverter(manager, output, laparams=LAParams())
#         interpreter = PDFPageInterpreter(manager, converter)
#
#         # file_ = open(os.path.join(BASE_DIR, 'sample.pdf'))
#         infile = file(pdffile, 'rb')
#         for page in PDFPage.get_pages(infile, pagenums):
#             interpreter.process_page(page)
#         infile.close()
#         converter.close()
#         text = output.getvalue()
#         emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
#
#         phone = re.findall(r"([^\d])\d{10}([^\d])", text)
#         # print ("hello")
#         print(emails)
#         if emails:
#             return emails
#         if phone:
#             return phone
#         else:
#             return ''
#
#             # text = convert()
#             # emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
#             # print emails
#







def email_phonenumber(file_path):

    data = textract.process(file_path)
    data1=data.decode("utf-8")
    # nlp = en_core_web_sm.load()
    # doc_2 = nlp(data1)
    # names=[]

    # stop_words = set(stopwords.words('english'))
    # word_tokens = word_tokenize(data1)
    # tokenizer = RegexpTokenizer(r'\w+')
    # tokens = tokenizer.tokenize(data1)
    # global filtered_sentence
    # filtered_sentence = [w for w in tokens if not w in stop_words]
    # print(filtered_sentence,"this s aaaaaasssdfffffgdcvm ikfg dhgvfe jgfudvdvf dgfie ........................")

    emails = re.findall(r"[A-Za-z0-9\.\-+_]+@[A-Za-z0-9\.\-+_]+\.[a-z]+", data1)
    s = re.findall(r'((?:\+|00)[17](?: |\-)?|(?:\+|00)[1-9]\d{0,2}(?: |\-)?|(?:\+|00)1\-\d{3}(?: |\-)?)?(0\d|\([0-9]{3}\)|[1-9]{0,3})(?:((?: |\-)[0-9]{2}){4}|((?:[0-9]{2}){4})|((?: |\-)[0-9]{3}(?: |\-)[0-9]{4})|([0-9]{7}))',data1)
    # name=""
    # for ent in doc_2.ents:
    #     if ent.label_ == "PERSON":
    #         names.append(format(ent))
    #         name=names[0]
    # if not name:
    #     name=""
    # else:
    #     name=names[0]

    if not s:
        phone_num = ""
    else:
        st = ''.join(s[0])
        phone_num=st.replace(" ", "")
    if not emails:
        email = ""
    else:
        email=emails[0]

    print(int(round(time.time() * 1000)),"end time")

    return (email,phone_num)


import os

from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import Q
from django.conf import settings
from django.db.models import FileField
@method_decorator(csrf_exempt, name='dispatch')
class OverwriteStorage(View,BaseCommand):

    def post(self,request):

            dat = []
            data=[]
            email_id={}
            phone_id={}
            unextracted_files=[]
            count=0
            finalized_count=0

            # time = now.strftime("%c")
            global company_name
            company_name = request.user.company.company_name
            myfile = request.FILES.getlist('docfile')
            # print(request.FILES,"&&&&&&&&&&&777")
            # print(myfile,"***************")
            file_count=request.POST.get('filecount')

            # print(file_count,"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            folder = "media/"+company_name
            fs = FileSystemStorage(location=folder)
            email_list=[]
            phone_list=[]
            def get_file_path(self,request):
                return settings.MEDIA_ROOT+"/"+ company_name + "/{}"


            for i in myfile:
                filename = fs.save(i.name, i)
                res=str(filename)

                mediapath=get_file_path(self,request)
                print(mediapath)
                filepath=os.path.join(BASE_DIR, mediapath).format(filename)
                print(filepath)
                saving_file_path = company_name +"/"+ filename
                if res.endswith('.pdf'):
                    data = email_phonenumber(filepath)
                    email = data[0]
                    phone1 = data[1]
                    print(phone1)
                    phone = re.sub('[^ a-zA-Z0-9]', '', phone1)
                    print(phone, "phone number")
                    # name=data[2]
                    try:
                        profile_path = Profile.objects.filter(
                            Q(candidate_email=email) & Q(added_for_id=request.user.company.id)).values_list(
                            'resume_path', ).first()
                        print(profile_path[0], "from db")
                        remove_profle_parh = settings.MEDIA_ROOT + "/" + str(profile_path[0])
                        profile = Profile.objects.filter(
                            Q(candidate_email=email) & Q(added_for_id=request.user.company.id)).values_list(
                            "id").first()
                        updated_profile = Profile.objects.get(id=profile[0])
                        print(updated_profile, "ffffffffffffffffffffffff")

                        updated_profile.resume_path = saving_file_path
                        updated_profile.resume_name = filename
                        updated_profile.save()
                        os.remove(remove_profle_parh)

                        print("successfull")
                    except:

                        result={"email":email,"phonenumber":phone,"name":""}
                        profile=Profile.objects.filter(added_for_id=request.user.company.id).values_list('candidate_email',flat=True)
                        if (result["email"] in list(profile)):
                            profile = Profile.objects.filter(candidate_email=result["email"], latest=True)
                            profile.update(latest=False)
                        dat.append(result)

                        if (email is "" and phone is "") or (email is "" or phone is ""):
                            print("coming here****************")
                            profile = Profile.objects.create(candidate_email=email, phone_number=phone,
                                                             resume_path=saving_file_path,
                                                             created_by_id=request.user.id,
                                                             updated_by_id=request.user.id, primary_skills="",
                                                             candidate_name="", expected_ctc="", current_company="",
                                                             notice_period="", percent_rise="",
                                                             added_for_id=request.user.company.id,
                                                             resume_name=res, updated_on=time,
                                                             experience="", current_ctc="", extracted_words="",
                                                             location="",
                                                             )
                            profile.save()
                        else:
                            profile = Profile.objects.create(candidate_email=email, phone_number=phone,
                                                             resume_path=saving_file_path, created_by_id=request.user.id,
                                                             updated_by_id=request.user.id, primary_skills="",
                                                             candidate_name="", expected_ctc="", current_company="",
                                                             notice_period="", percent_rise="",
                                                             added_for_id=request.user.company.id,
                                                             resume_name=res, updated_on=time,
                                                             experience="", current_ctc="", extracted_words="",
                                                             location="",
                                                             )
                            profile.save()



                elif res.endswith('.docx'):
                    data = email_phonenumber(filepath)
                    email = data[0]
                    phone1 = data[1]
                    print(phone1)
                    phone = re.sub('[^ a-zA-Z0-9]', '', phone1)
                    print(phone, "phone number")
                    # name=data[2]
                    try:
                        profile_path = Profile.objects.filter(
                            Q(candidate_email=email) & Q(added_for_id=request.user.company.id)).values_list(
                            'resume_path', ).first()
                        print(profile_path[0], "from db")
                        remove_profle_parh = settings.MEDIA_ROOT + "/" + str(profile_path[0])
                        profile = Profile.objects.filter(
                            Q(candidate_email=email) & Q(added_for_id=request.user.company.id)).values_list(
                            "id").first()
                        updated_profile = Profile.objects.get(id=profile[0])
                        print(updated_profile, "ffffffffffffffffffffffff")

                        updated_profile.resume_path = saving_file_path
                        updated_profile.resume_name = filename
                        updated_profile.save()
                        os.remove(remove_profle_parh)

                        print("successfull")
                    except:

                        result = {"email": email, "phonenumber": phone,"name":""}
                        profile = Profile.objects.filter(added_for_id=request.user.company.id).values_list(
                            'candidate_email', flat=True)
                        if (result["email"] in list(profile)):
                            profile = Profile.objects.filter(candidate_email=result["email"], latest=True)
                            profile.update(latest=False)
                        dat.append(result)

                        if (email is "" and phone is "") or (email is "" or phone is ""):
                            print("coming here****************")
                            profile = Profile.objects.create(candidate_email=email, phone_number=phone,
                                                             resume_path=saving_file_path,
                                                             created_by_id=request.user.id,
                                                             updated_by_id=request.user.id, primary_skills="",
                                                             candidate_name="", expected_ctc="", current_company="",
                                                             notice_period="", percent_rise="",
                                                             added_for_id=request.user.company.id,
                                                             resume_name=res, updated_on=time,
                                                             experience="", current_ctc="", extracted_words="",
                                                             location="",
                                                             )
                            profile.save()
                        else:
                            profile = Profile.objects.create(candidate_email=email, phone_number=phone,
                                                             resume_path=saving_file_path,
                                                             created_by_id=request.user.id,
                                                             updated_by_id=request.user.id, primary_skills="",
                                                             candidate_name="", expected_ctc="", current_company="",
                                                             notice_period="", percent_rise="",
                                                             added_for_id=request.user.company.id,
                                                             resume_name=res, updated_on=time,
                                                             experience="", current_ctc="", extracted_words="",
                                                             location="",
                                                             )
                            profile.save()



                elif res.endswith('.doc'):
                    data = email_phonenumber(filepath)
                    email = data[0]
                    phone1 = data[1]
                    print(phone1)
                    phone = re.sub('[^ a-zA-Z0-9]', '', phone1)
                    print(phone, "phone number")
                    # name=data[2]
                    try:
                        profile_path = Profile.objects.filter(
                            Q(candidate_email=email) & Q(added_for_id=request.user.company.id)).values_list(
                            'resume_path', ).first()
                        print(profile_path[0], "from db")
                        remove_profle_parh = settings.MEDIA_ROOT + "/" + str(profile_path[0])
                        profile = Profile.objects.filter(
                            Q(candidate_email=email) & Q(added_for_id=request.user.company.id)).values_list(
                            "id").first()
                        updated_profile = Profile.objects.get(id=profile[0])
                        print(updated_profile, "ffffffffffffffffffffffff")

                        updated_profile.resume_path = saving_file_path
                        updated_profile.resume_name = filename
                        updated_profile.save()
                        os.remove(remove_profle_parh)

                        print("successfull")
                    except:

                        result = {"email": email, "phonenumber": phone,"name":""}
                        profile = Profile.objects.filter(added_for_id=request.user.company.id).values_list(
                            'candidate_email', flat=True)
                        if (result["email"] in list(profile)):
                            profile = Profile.objects.filter(candidate_email=result["email"], latest=True)
                            profile.update(latest=False)
                        dat.append(result)
                        if (email is "" and phone is "") or (email is "" or phone is ""):
                            print("coming here****************")
                            profile = Profile.objects.create(candidate_email=email, phone_number=phone,
                                                             resume_path=saving_file_path,
                                                             created_by_id=request.user.id,
                                                             updated_by_id=request.user.id, primary_skills="",
                                                             candidate_name="", expected_ctc="", current_company="",
                                                             notice_period="", percent_rise="",
                                                             added_for_id=request.user.company.id,
                                                             resume_name=res, updated_on=time,
                                                             experience="", current_ctc="", extracted_words="",
                                                             location="",
                                                             )
                            profile.save()

                        else:
                            profile = Profile.objects.create(candidate_email=email, phone_number=phone,
                                                             resume_path=saving_file_path,
                                                             created_by_id=request.user.id,
                                                             updated_by_id=request.user.id, primary_skills="",
                                                             candidate_name="", expected_ctc="", current_company="",
                                                             notice_period="", percent_rise="",
                                                             added_for_id=request.user.company.id,
                                                             resume_name=res, updated_on=time,
                                                             experience="", current_ctc="", extracted_words="",
                                                             location="",
                                                             )
                            profile.save()


                elif res.endswith('.odt'):
                    data = email_phonenumber(filepath)
                    email = data[0]
                    phone1 = data[1]
                    print(phone1)
                    phone = re.sub('[^ a-zA-Z0-9]', '', phone1)
                    print(phone, "phone number")
                    # name=data[2]
                    try:
                        profile_path = Profile.objects.filter(
                            Q(candidate_email=email) & Q(added_for_id=request.user.company.id)).values_list(
                            'resume_path', ).first()
                        print(profile_path[0], "from db")
                        remove_profle_parh = settings.MEDIA_ROOT + "/" + str(profile_path[0])
                        profile = Profile.objects.filter(
                            Q(candidate_email=email) & Q(added_for_id=request.user.company.id)).values_list(
                            "id").first()
                        updated_profile = Profile.objects.get(id=profile[0])
                        print(updated_profile, "ffffffffffffffffffffffff")

                        updated_profile.resume_path = saving_file_path
                        updated_profile.resume_name = filename
                        updated_profile.save()
                        print("outside")

                        os.remove(remove_profle_parh)

                        print("successfull")
                    except:

                        result = {"email": email, "phonenumber": phone, "name": ""}
                        profile = Profile.objects.filter(added_for_id=request.user.company.id).values_list(
                            'candidate_email', flat=True)
                        if (result["email"] in list(profile)):
                            profile = Profile.objects.filter(candidate_email=result["email"], latest=True)
                            profile.update(latest=False)
                        dat.append(result)

                        if (email is "" and phone is "") or (email is "" or phone is ""):
                            print("coming here****************")
                            profile = Profile.objects.create(candidate_email=email, phone_number=phone,
                                                             resume_path=saving_file_path,
                                                             created_by_id=request.user.id,
                                                             updated_by_id=request.user.id, primary_skills="",
                                                             candidate_name="", expected_ctc="", current_company="",
                                                             notice_period="", percent_rise="",
                                                             added_for_id=request.user.company.id,
                                                             resume_name=res,
                                                             experience="", current_ctc="", extracted_words="",
                                                             location="",
                                                             )
                            profile.save()


                        else:
                            profile = Profile.objects.create(candidate_email=email, phone_number=phone,
                                                             resume_path=saving_file_path,
                                                             created_by_id=request.user.id,
                                                             updated_by_id=request.user.id, primary_skills="",
                                                             candidate_name="", expected_ctc="", current_company="",
                                                             notice_period="", percent_rise="",
                                                             added_for_id=request.user.company.id,
                                                             resume_name=res, updated_on=time,
                                                             experience="", current_ctc="", extracted_words="",
                                                             location="",
                                                             )
                            profile.save()

                else:
                    count=count+1
                    unextracted_files.append(res)

            print(count,"333333333333333333333")

            final_count=count
            print(type(final_count),"@@@@@@@@@@@@@22")
            print(type(file_count),"%%%%%%%%%%%%%%%%%")
            fc=int(file_count)
            print(final_count,")00000000")
            if final_count >= 0:
                finalized_count=fc-final_count
                print(finalized_count,"%%%%%%%%%%%%%%%%%5")
                var=str(finalized_count) +" profiles extracted out of "+str(file_count)
                print(final_count,"++++++++++++++++++++++++++++=s")
                print(var)
                dat={"msg" : var ,"list":unextracted_files}
                print(dat, "aaaaaaaaaaaaaaaaaaaaccccccccccccccccccccccccccccccccc")
            return JsonResponse(dat, safe=False)




            return render(request, "customerlist.html")

#
# class Searchprofiles(View) :
#    def get(self,request):
#
#        list1=[]
#
#
#        profile = Profile.objects.filter(added_for_id=request.user.company_id).values('resume_path','resume_name')
#
#
#        temo=[p["resume_path"] for p in profile]
#        list2=temo
#        all_skill_resume = []
#        all_skill_count=[]
#        indi_skill_count=[]
#        indi_skill_resume = []
#        for resume in list2 :
#            data = textract.process(resume)
#            data1=data.decode("utf-8")
#            skills_find=request.GET.get("profiles").split(',')
#            skills_find=set(skills_find)
#            print(skills_find,"**************")
#            resume_name = resume.split('/')[-1]
#            skill_found=0
#            for skill in skills_find:#loop all skills
#                if re.search(skill.strip(), data1, re.IGNORECASE):
#                    list1.append(resume)
#
#                    count =  len(re.findall(skill.strip(), data1, re.IGNORECASE))
#                    skill_found+=1
#                    if int(len(skills_find)) == int(skill_found):
#                        all_skill_resume.append([resume_name,skills_find])
#                        all_skill_count.append({'resume_name':resume_name,'skills':skill,'count':count})
#
#                    if count > 0:
#                        indi_skill_resume.append([resume_name,skill,count])
#                        indi_skill_count.append({'resume_name':resume_name,'skills':skill,'count':count})
#                        indi_skill_resume = sorted(indi_skill_resume, key=lambda x: x[2], reverse=True)
#
#        print(all_skill_resume)
#        print(indi_skill_resume)
#        print(all_skill_count,"this is a dictionary")
#        print(indi_skill_count,"this is a new dictionary")
#
#
#
#                        # print(list1 , "this shoud show")
#
#
#
#                        # if request.GET.get("skills") in data1:
#                        #     list1.append(i)
#        company = Company.objects.filter(parent_company_id=request.user.company_id).values_list("id", flat=True)
#        profile = Profile.objects.filter(resume_path__in=[pr for pr in list1]).values_list("candidate_name","candidate_email","phone_number",
#                                                                                                                              "primary_skills",
#                                                                                                                              "current_company",
#                                                                                                                              "experience",
#                                                                                                                              "current_ctc",
#                                                                                                                              "expected_ctc" ,
#                                                                                                                                 "notice_period",
#                                                                                                                               "updated_on",
#                                                                                                                               "resume_name",
#                                                                                                                                     )
#        data = [ {'name' : p[0],'email':p[1],'phone':p[2],'skills':p[3],'comp':p[4],'exp':p[5],'ctc':p[6],'expctc':p[7],'notice':p[8],'update':p[9],'resume_name':p[10]} for p in profile ]
#        print(data)
#
#
#        return JsonResponse(data,safe=False)
