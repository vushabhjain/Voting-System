from OVS import settings  
from django.core.mail import EmailMessage 

def SendEmail(Voter_Id,Email_Id,Password):
    msg     = f"<h4>Your Voter Id is = {Voter_Id} and password is {Password}</h4>"  
    to      = [Email_Id]  
    # res     = send_mail(subject, msg, settings.EMAIL_HOST_USER,to)
    email=settings.EMAIL_HOST_USER
    user = Email_Id
    email_body = """\
    <html>
      <head></head>
      <body>
        <h2>%s</h2>
        <p>%s</p>
        <h5>%s</h5>
      </body>
    </html>
    """ % (user, msg, email)
    email = EmailMessage('A new mail!', email_body, to=to)
    email.content_subtype = "html" # this is the crucial part 
    res = email.send()
    flag = 0  
    if(res == 1):  
        msg = "Mail Sent Successfuly" 
        flag = 1
        return msg,flag
    else:  
        msg = "Mail could not sent"  
        return msg, flag
    
def MailToNonVoters(Email_Id):
    msg = f"<h4>You did not vote please vote"  
    to  = [Email_Id]  
    email=settings.EMAIL_HOST_USER
    user = Email_Id
    email_body = """\
    <html>
      <head></head>
      <body>
        <h2>%s</h2>
        <p>%s</p>
        <h5>%s</h5>
      </body>
    </html>
    """ % (user, msg, email)
    email = EmailMessage('A new mail!', email_body, to=to)
    email.content_subtype = "html" # this is the crucial part 
    res = email.send()
    flag = 0  
    if(res == 1):  
        msg = "Mail Sent Successfuly" 
        flag = 1
        return msg,flag
    else:  
        msg = "Mail could not sent"  
        return msg, flag