from django.shortcuts import render,redirect
from django.http import HttpResponse
from OVSapp.models import UserModel,AppealModel,ElectionYearModel,VotingsModel,VotingHistoryModel,profileModel
from OVSapp.functions import SendEmail,MailToNonVoters
from django.contrib.sessions.models import Session
import string
import random

#---------------- HTML Page rendering view functions ----------------
def index(request):
    return render(request,'login.html',{})

def Home(request):
    return render(request,'index.html',{})

def SignupForm(request): 
    return render(request,'signup.html',{})

def admin1(request):
    users = UserModel.objects.filter(status=1)
    users = len(users)
    return render(request,'admin.html',{'users':users})

def appealForm(request):
    return render(request,"appeal.html",{})

def StartElectionsForm(request):
    election_data = ElectionYearModel.objects.all()
    return render(request,'startelections.html',{"data":election_data})

# This view function will show list of accepted users on admin side
def userList(request):
    requests = UserModel.objects.filter(status=1).values()
    return render(request,"userlist.html",{"requests":requests})

#------------------------ End Of HTML Page rendering view functions ----------------------------





#-------------------------------- Login & Signup Module ----------------------------------------

""" StoreUser() is used for storing the data of Singup Module, this data will go as a request to admin and
when admin accepts the request then only user will be able to login or he will redirected to appeal page. 
LoginUser() is used to search user using its username and password, this function parses through the 
databases and fetches the required record, if the admin has accepted the request then user will successfully 
login or he will be redirected to appeal page. """

def StoreUser(request): 
    if request.method == "POST":
        Full_Name= request.POST.get('name')
        Email_Id = request.POST.get('email')
        Phone= request.POST.get('phone')
        Aadhar_Id = request.POST.get('Aadhar')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        model = UserModel(Full_Name=Full_Name,Email_Id=Email_Id,Phone=Phone,Aadhar_Id=Aadhar_Id,Password=pass1)
        if pass1 == pass2:
            model.save()
            return redirect('/')
        else:
            msg = "password does not match"
            flag = 1
            return render(request,'signup.html',{'msg':msg,'flag':flag})
        

def LoginUser(request):
    if request.method == "POST":
        Email_Id = request.POST.get('username')
        Password = request.POST.get('password')
        datas = UserModel.objects.filter(Email_Id=Email_Id,Password=Password).values()
        if Email_Id == "admin" and Password == "admin":
            return redirect("/admin1")
        elif len(datas) == 1:
            if datas[0]['status'] == 1:
                request.session['name1'] = datas[0]['Full_Name']
                request.session['uid'] = datas[0]['User_Id']
                return redirect('/Home')
            elif datas[0]['status'] == 2:
                request.session['name1'] = datas[0]['Full_Name']
                request.session['uid'] = datas[0]['User_Id']
                return redirect('/appealForm')
            else:
                flag = 2
                message = "Cannot Login, Admin has not approved your request yet"
                return render(request,"login.html",{"message":message,"flag":flag})
        else:
            flag = 1
            msg = "Login Failed"
            return render(request,"login.html",{"msg":msg,"flag":flag})
                
#------------------------- End Of Login & Signup Module -----------------------------

                
                


#----------------------------- Login Request Module ---------------------------------
""" LoginRequest() will show the list of all rejected users to admin side.
RequestAccepted() when called will change status of user and it will automatically generate voter ID
and send it through mail to that User.
RequestRejected() when called will change the status of user to 2 which represents 'Rejected' and User
will not be able to login. """

def LoginRequest(request):
    requests = UserModel.objects.filter(status=0).values()
    return render(request,"loginrequest.html",{"requests":requests})


def RequestAccepted(request,action_id):
    request = UserModel.objects.get(User_Id=action_id)
    size = 3
    # Code below will generate random alphabets string
    random_alphabets = random.choices(string.ascii_uppercase,k = size)
    strings = ""
    for alphabet in random_alphabets:
        strings = strings + alphabet
    # Code below will generate random number string
    randomlist = random.sample(range(0,9),7)
    Number = map(str,randomlist)
    number_list = list(Number)
    Number_String = ""
    for number in number_list:
        Number_String = Number_String + number
    # Code will generate and save Voter ID in database
    Voter_Id = strings + Number_String
    request.Voter_Id = Voter_Id
    request.status = 1
    request.save()
    Voter_Id = request.Voter_Id
    Email_id = request.Email_Id
    Password = request.Password
    flag,msg = SendEmail(Voter_Id,Email_id,Password)
    return redirect('/LoginRequest')

           
def RequestRejected(request,action_id):
    req = UserModel.objects.get(User_Id=action_id)
    req.status = 2
    req.save()
    return redirect('/LoginRequest')

#----------------------------- End of Login Request Module --------------------------------





#------------------------------------ Appeal Module ---------------------------------------
""" Appeal() will store the appeal message typed and submitted by rejected users,appeallist() will
show all the appeals from users to admin side, when admin accepts a users appeal the appealAccepted()
will change the status of user and user will be able to login and appealDelete() will delete the appeal
of user. """

def appeal(request):
    if request.method == 'POST':
        msg = request.POST.get('msg')
    name = request.session['name1']
    user_id = request.session['uid']
    model = AppealModel(Name=name,Message=msg,user_id=user_id)
    model.save()
    msg = "Appeal sent successfully"
    flag = 1
    return render(request,"appeal.html",{'msg':msg,'flag':flag})

def appealList(request):
    appeals = AppealModel.objects.all()
    return render(request,"appeallist.html",{'appeals':appeals})

def appealAccepted(request,Appeal_Id):
    appeal = AppealModel.objects.get(Appeal_Id=Appeal_Id)
    user_id = appeal.user_id
    users = UserModel.objects.get(User_Id=user_id)
    size = 3
    # Code below will generate random alphabets string
    random_alphabets = random.choices(string.ascii_uppercase,k = size)
    strings = ""
    for alphabet in random_alphabets:
        strings = strings + alphabet
    # Code below will generate random number string
    randomlist = random.sample(range(0,9),7)
    Number = map(str,randomlist)
    number_list = list(Number)
    Number_String = ""
    for number in number_list:
        Number_String = Number_String + number
    # Code will generate and save Voter ID in database
    Voter_Id = strings + Number_String
    users.Voter_Id = Voter_Id
    Voter_Id = users.Voter_Id
    Email_id = users.Email_Id
    Password = users.Password
    flag,msg = SendEmail(Voter_Id,Email_id,Password)
    users.status = 1
    users.save()
    appeal.delete()
    return redirect('/appealList')
        
def appealDelete(request,Appeal_Id):
    appeal= AppealModel.objects.get(Appeal_Id=Appeal_Id)
    appeal.delete()
    return redirect('/appealList')

#----------------------------- End of Appeal Module ----------------------------------





#--------------------------------- Graph Module --------------------------------------
""" Graph() will get all years data from Election_Year table and pass it to graphs.html 
GenerateGraph() generates graphs based on votings. """

def Graphs(request):
    years = ElectionYearModel.objects.all()
    return render(request,'graphs.html',{'years':years})


def GenerateGraph(request):
    if request.method == "POST":
        year = request.POST.get('year')
        datas = VotingHistoryModel.objects.filter(year=year)
        for data in datas:
            year = data.vhid
        data = VotingHistoryModel.objects.get(vhid=year)
        bjp = data.bjp
        cong = data.cong
        aap = data.aap
        year = data.year
        flag =1
        years = ElectionYearModel.objects.all()
        return render(request,'graphs.html',{'bjp':bjp,'cong':cong,'aap':aap,'year':year,'flag':flag,'years':years})

#------------------------------- End Of Graph Module -----------------------------------





# -------------------------------- Election Module -------------------------------------
""" StartElection() will start a new election only if another election is not going on and for this to
happen StartElection() will first check in table and if it does not find any year with status 1 then 
it will start a new election or it will execute another If block.

StopElection() when called will change the status of that year to 0 which indicated that elections for
that year is stopped and no votings can be done further, after stopping election StopElection() will 
calculate all votes and store them in Voting_History table in their respective parties fields. """

def StartElections(request):
    if request.method == "POST":
        year = request.POST.get('year')
        election =  ElectionYearModel.objects.filter(status=1)
        if len(election) == 0:
            model = ElectionYearModel(year=year,status=1)
            model.save()
            voters = UserModel.objects.filter(Voting_Score=1)
            for voter in voters:
                voter1 = voter.User_Id
                user = UserModel.objects.get(User_Id=voter1)
                user.Voting_Score = 0
                user.save()
            return redirect('/StartElectionsForm')
        if len(election) >= 1:
            msg = 'Cannot start new election as a election is still going on'
            flag = 1
            election_data = ElectionYearModel.objects.all()
            return render(request,'startelections.html',{'msg':msg,'flag':flag,'data':election_data})
        else:
            msg = 'error'
            flag = 2
            return render(request,'startelections.html',{'msg':msg,'flag':flag})
        
        
def StopElections(request,elec_id):
    election = ElectionYearModel.objects.get(elec_id=elec_id)
    year = election.year
    bjp = len(VotingsModel.objects.filter(party='bjp'))
    cong = len(VotingsModel.objects.filter(party='cong'))
    aap = len(VotingsModel.objects.filter(party='aap'))
    model = VotingHistoryModel(bjp=bjp,cong=cong,aap=aap,year=year)
    model.save()
    election.status=0
    election.save()
    VotingsModel.objects.all().delete()
    return redirect('/StartElectionsForm')


def DeleteYear(request,elec_id):
    year = ElectionYearModel.objects.get(elec_id=elec_id)
    year.delete()
    return redirect("/StartElectionsForm")
#------------------------------- End Of Election Module ----------------------------------





#------------------------------------ Voting Module --------------------------------------
""" Vote() will check if any election is going on and if elections are being held then it willshow list 
of Political parties for voting and if no elections are held then it will execute else block.

VoteParty() will store the name of the voter and the name of party to which the user has voted into 
Votings Table and further more the VoteParty() will get the record of that user from Tbl_User table and
change its Voting_Score to 1 which indicates that the user has voted and he will not be able to vote again. """
    
def Vote(request):
    election = ElectionYearModel.objects.filter(status=1)
    if len(election) == 1:
        for ele in election:
            year = ele.year
        election = ElectionYearModel.objects.get(year=year)
        Vote_Status = election.status
        Year = election.year
        return render(request,'vote.html',{'vote':Vote_Status,'year':Year})
    else:
        msg = "No elections are being held right now"
        return render(request,'vote.html',{'msg':msg})
    
    
def VoteParty(request,party):
    Party = party    
    name = request.session['name1']
    uid = request.session['uid']
    user = UserModel.objects.get(User_Id=uid)
    user.Voting_Score = 1
    user.save()
    user = user.Voting_Score
    model = VotingsModel(name=name,party=Party)
    model.save()
    return render(request,'index.html',{'user':user})  

#------------------------------ End of Voting Module -------------------------------- 





#--------------------------- Mailing to Non Voters Module ----------------------------
""" Not_Voted() will list all the registered users who has not voted in ongoing elections and after the
elections on admin side.

SendMailToNonVoters() when called will get the record of the user from Tbl_Users Table and then it will
send a mail to that user automatically regarding non voting. """

def Not_Voted(request):
    year = ElectionYearModel.objects.filter(status=1)
    year = len(year)
    if year == 1:
        votes = UserModel.objects.filter(Voting_Score=0)
        tag = 'Ongoing'
        return render(request,'notvoted.html',{'votes':votes,'tag':tag})
    else:
        votes = UserModel.objects.filter(Voting_Score=0)
        tag = 'After Elections'
        return render(request,'notvoted.html',{'votes':votes,'tag':tag})
    
    
def SendMailToNonVoters(request,User_Id):
    User = UserModel.objects.get(User_Id=User_Id)
    Email_Id = User.Email_Id
    mail = MailToNonVoters(Email_Id)
    return redirect('/Not_Voted')

#----------------------- End Of Mailing to Non Voters Module -------------------------





#--------------------------------- Profile Module ------------------------------------
""" ProfileView() will first check if the Profile table is empty then try block will be executed which
will redirect user to Create Profile page, but if the user already has profile created then he will
directly see his profile, and if a new user clicks on Profile the except block will be executed and he 
will be redirected to Create Profile Page. 

createprofileForm() renders the createprofile.html file.

createProfile() will get all data from createprofile.html file and store it in Profile table.

ProfileUpdateForm() will render profileEdit.html file and some fields will already be filled and then user
can edit those fields as per his/her requirements.

ProfileUpdate() will get all data from profileEdit.html file and it will store updated data in Profile Table.
"""
def ProfileView(request):
    uid = int(request.session['uid'])
    profiles = profileModel.objects.all()
    num = len(profiles)
    try:
        if num == 0:
            flag = 1
            request.session['flag'] = flag
            return redirect('/createprofileForm')
        else:      
            prof = profileModel.objects.get(User=uid) 
            return render(request,"profile.html",{"prof":prof,"uid":uid})
    except:
        return redirect('/createprofileForm')
    
            
def createprofileForm(request):
    return render(request,"createprofile.html",{})


def createProfile(request):
     if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        uid = int(request.session['uid'])
        User = UserModel.objects.get(User_Id=uid)
        request.session['name'] = name
        prof = profileModel(name=name,email=email,phone=phone,address=address,image=image,User=User)
        prof.save()
        request.session['flag'] = 0
        return redirect('/ProfileView')
     

def ProfileUpdateForm(request):
    uid = int(request.session['uid'])
    prof = profileModel.objects.get(User=uid)
    return render(request,"ProfileEdit.html",{'prof':prof})


def ProfileUpdate(request):
   if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        uid = int(request.session['uid'])
        request.session['name'] = ''
        data = profileModel.objects.get(User=uid)
        data.name=name
        data.email=email
        data.address=address
        data.image=image
        data.phone=phone
        data.save()
        return redirect('/ProfileView')
   
#--------------------------- End Of Profile Module ----------------------------