
from django.conf.urls import url
from .views import Log_screen, Landingscreen,login_user, operator, logout_user, customers, customerpage,  updateprofile, updatecust, attachprofiles, profiledetails, updateoperator, Conversations, ConversationDisplay, DeleteOperator,\
operatorsJobListing,Checkcompany,StatusUpdate,CheckMail,Checkcompanyoperator,ResetPassword,OperatorDetails,AddOperator,ChangePassword,html_to_excel_view,OperatorListToExcle,ProfileListToExcle,JpaListToExcle,JobProfileAssociationDelete,DeleteProfiles,Sendmail_withAxcel,html_to_excel_view_email,DeleteJob,Attach_excel_to_mail,DeleteUnAttachedProfile,UpdateJob,JobDetailsShow,ProfileRepositoryLoad,ProfileDetailsShow,ProfileAttachCheck,GetAllSkills,GetDashboardDetails,Dashboard_to_excel,Userlist_to_excel,CustomerJobList_to_excel,GetAllJobs,CompanyJoblist,operatorcreatejob,CreateNotes,AllJobStatus,DownloadProfile,MyUserUpdate,CheckPrimaryUser,Customerchecked

urlpatterns = [


    url(r'^$', view=Landingscreen.as_view(),name="screen"),
    url(r'^logscreen/',view=Log_screen.as_view(),name="logs"),
    url(r'^login/', view=login_user,name="login"),
    url(r'^operatorlist/', view=operator,name="operatorlist"),
    url(r'^logout/',view=logout_user,name='logout'),
    url(r'^operatorpage/', view=customers, name='operatorpage'),
    #url(r'^customerpage/(?P<id>\d+)/$', customerpage, name='customerpage'),
    # url(r'^operator/customerpage/(?P<companyid>\d+)/$',operatorjob, name='operatorcustomerpage'),
    url(r'^operator/joblist/(?P<companyid>\d+)/$',operatorsJobListing, name='operatorcustomer'),
    url(r'^company/joblist/', CompanyJoblist.as_view(), name='operatorcustomer'),

    url(r'^customerpage/',customerpage, name='customerpage'),
    url(r'^operator/customerpage/$',operatorcreatejob, name='operatorcustomerpagepost'),
    url(r'^operatorcreatejob/$',operatorcreatejob, name='operatorcreatejob'),

    url(r'^updateprofile/', view=updateprofile, name="updateprofile"),
    url(r'^updatecustomer/', view=updatecust, name="updatecustomer"),
    url(r'^updateoperator/',view=updateoperator,name="updateoperator"),

    url(r'^profiledetails/$', view=profiledetails, name='profiledetails'),

    url(r'^operatorpage/(?P<jobid>\d+)/$', view=customers, name='operatorpagejob'),

    url(r'^attachprofiles/$', view=attachprofiles, name='attachprofiles'),


    url(r'^attachprofiles/$', view=attachprofiles, name='attachprofilespost'),

    url(r'^conversation/$',view=Conversations.as_view(), name='conversation'),
    url(r'^conversationdisplay/$', view=ConversationDisplay.as_view(), name='conversationdisplay'),
    url(r'^checkcompany/$', view=Checkcompany.as_view(), name='checkcompany'),
    url(r'^deleteoper/$', view=DeleteOperator.as_view(), name='deleteoper'),
    url(r'^statusupdate/$', view=StatusUpdate.as_view(), name='statusupdate'),
    url(r'^ckeckmail/$', view=CheckMail.as_view(), name='ckeckmail'),
    url(r'^checkcompanyoperator/$', view=Checkcompanyoperator.as_view(), name='checkcompanyoperator'),
    url(r'^resetpassword/$', view=ResetPassword.as_view(), name='reset'),
    url(r'^operatorsdetails/', view=OperatorDetails.as_view(), name='operatorsdetails'),
    url(r'^addoperator/', view=AddOperator.as_view(), name='addoperator'),
    url(r'^changepassword/', view=ChangePassword.as_view(), name='changepassword'),
    url(r'^operatorlisttoexcel/$', html_to_excel_view, name='operatorlisttoexcel'),
    url(r'^operatorlisttoexcel_email/$', html_to_excel_view_email, name='operatorlisttoexcel_email'),

    url(r'^customerlisttoexcel/$', OperatorListToExcle.as_view(), name='customerlisttoexcel'),
    url(r'^profilelisttoexcel/$', ProfileListToExcle.as_view(), name='profilelisttoexcel'),
    url(r'^jpalisttoexcel/$', JpaListToExcle.as_view(), name='jpalisttoexcel'),
    url(r'^dashboardtoexcel/$', Dashboard_to_excel.as_view(), name='dashboardtoexcel'),
    url(r'^userlisttoexcel/$', Userlist_to_excel.as_view(), name='userlisttoexcel'),
    url(r'^customerjoblisttoexcel/$', CustomerJobList_to_excel.as_view(), name='customerjoblisttoexcel'),

    url(r'^deleteprofile/$', DeleteProfiles.as_view(), name='deleteprofile'),

    url(r'^deletejobprofile/$', view=JobProfileAssociationDelete.as_view(), name='deletejobprofile'),
    url(r'^attach_excel/$', view=Sendmail_withAxcel.as_view(), name='attach_excel'),
    url(r'^attachexcel_tomail/$', view=Attach_excel_to_mail.as_view(), name='attachexcel_tomail'),
    url(r'^deletejobs/$', view=DeleteJob.as_view(), name='deletejobs'),
    url(r'^deleteunattchedprofile/$', view=DeleteUnAttachedProfile.as_view(), name='deleteunattchedprofile'),
    url(r'^updatejob/$', view=UpdateJob.as_view(), name='updatejob'),
    url(r'^job_details_show/$', view=JobDetailsShow.as_view(), name='job_details_show'),
    url(r'^loadprofilerepository/$', view=ProfileRepositoryLoad.as_view(), name='loadprofilerepository'),
    url(r'^show_profile_details/$', view=ProfileDetailsShow.as_view(), name='show_profile_details'),
    url(r'^checkingjob/$', view=ProfileAttachCheck.as_view(), name='checkingjob'),
    url(r'^getallskills/$', view=GetAllSkills.as_view(), name='getallskills'),
    url(r'^dashboarddetails/$', view=GetDashboardDetails.as_view(), name='dashboarddetails'),
    url(r'^getalljobs/$', view=GetAllJobs.as_view(), name='getalljobs'),
    url(r'^create_notes/$', view=CreateNotes.as_view(), name='create_notes'),
    url(r'^alljobstatus/$', view=AllJobStatus.as_view(), name='alljobstatus'),
    url(r'^downloadprofile/$', view=DownloadProfile.as_view(), name='downloadprofile'),
    url(r'^updatemyuser/$', view=MyUserUpdate.as_view(), name='updatemyuser'),
    url(r'^checkprimaryuser/$', view=CheckPrimaryUser.as_view(), name='checkprimaryuser'),
    url(r'^customer_checked/$', view=Customerchecked.as_view(), name='customer_checked'),

]

