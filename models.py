from django.db import models

# Create your models here.
class UserModel(models.Model):
    User_Id= models.AutoField(primary_key=True)
    Full_Name = models.CharField(max_length=30)
    Email_Id = models.CharField(max_length=50)
    Phone = models.CharField(max_length=10)
    Aadhar_Id = models.CharField(max_length=12)
    Voter_Id = models.CharField(max_length=10)
    status = models.IntegerField(default=0)
    Password= models.CharField(max_length=30)   
    Voting_Score = models.IntegerField(default=0) 
    
    class Meta:
        db_table= "Tbl_Users"

class AppealModel(models.Model):
    Appeal_Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=30)
    Message = models.CharField(max_length=200)
    user_id = models.IntegerField(default=0)

    class Meta:
        db_table = "Tbl_Appeal"

class ElectionYearModel(models.Model):
    elec_id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=4)
    status = models.IntegerField(default=0)

    class Meta:
        db_table = 'Election_Year'

class VotingsModel(models.Model):
    vid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    party = models.CharField(max_length=50)

    class Meta:
        db_table = 'Votings'

class VotingHistoryModel(models.Model):
    vhid = models.AutoField(primary_key=True)
    bjp = models.CharField(max_length=20)
    cong = models.CharField(max_length=20)
    aap = models.CharField(max_length=20)
    year = models.CharField(max_length=4)

    class Meta:
        db_table = "Voting_History"

class profileModel(models.Model):
    pid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    image = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    User = models.ForeignKey(UserModel, on_delete = models.CASCADE)

    class Meta:
        db_table = "Profile"