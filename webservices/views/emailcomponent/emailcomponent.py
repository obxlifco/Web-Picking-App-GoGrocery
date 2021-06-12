# from webservices.models import *
# from django.db.models import Q
# from webservices.serializers import *
# from rest_framework.views import APIView
# from rest_framework import generics
# from rest_framework.response import Response
# import socket
# from webservices.views import loginview
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from django.core.mail import EmailMessage
import sys,os
import traceback
from webservices.models import *
from webservices.serializers import *
from webservices.views.inventory.threading import *

def MailSettings():
    data = {}
    rs_settings = EngageboostGlobalSettings.objects.filter(isblocked='n', isdeleted = 'n').first()
    data = {
        "smtp_server":"smtp.office365.com",
        "smtp_port":587,
        "smtp_username":"support@gogrocery.ae",
        "smtp_password":"lifcoshop@123",
        "mail_sent_from":"support@gogrocery.ae",
        "mail_reply_to":"support@gogrocery.ae"
    }
    if rs_settings:
        data = {
            "smtp_server":rs_settings.smtp_server,
            "smtp_port":rs_settings.smtp_port,
            "smtp_username":rs_settings.smtp_username,
            "smtp_password":rs_settings.smtp_password,
            "mail_sent_from":rs_settings.mail_sent_from,
            "mail_reply_to":rs_settings.mail_reply_to
        }
    return data

def sendAppointmentMail(company_db,courier_email,email_subject,email_body,manifest="",attachment=None):
    # email_from == my email address
    # send_to == recipient's email address
    email_from = "subhasis.debnath@navsoft.in"
    send_to = courier_email

    #*****Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = email_subject
    msg['From'] = email_from
    msg['To'] = send_to

    #*****Create the body of the message (a plain-text and an HTML version).
    template = email_body
    # template += manifest
    # template = template.replace("{@name}","Subhasis Debnath")

    #*****Record the MIME types of both parts - text/plain and text/html.
    # part1 = MIMEText(text, 'plain')
    part2 = MIMEText(template, 'html')

    #*****Send attachment
    if attachment:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attachment,"rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
        msg.attach(part)

    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('subhasis.debnath@navsoft.in', 'sdchelsea')
    # mail.sendmail(email_from, send_to, msg.as_string())
    mail.sendmail(email_from, send_to, msg.as_string())
    mail.quit()
    data={"status":1}
    return data

def sendOrderMail(company_db,email_to,email_from,email_subject,email_body):
    # email_from == my email address
    # send_to == recipient's email address

    # email_from = email_from
    # send_to = email_to

    mail_settings = MailSettings()
    email_from = mail_settings.mail_sent_from
    send_to = email_to

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = email_subject
    msg['From'] = mail_settings['mail_sent_from']
    msg['To'] = send_to

    # Create the body of the message (a plain-text and an HTML version).
    template = email_body

    # Record the MIME types of both parts - text/plain and text/html.
    # part1 = MIMEText(text, 'plain')
    msg_content = MIMEText(template, 'html')
    msg.attach(msg_content)
    try:
        # Send the message via local SMTP server.
        mail = smtplib.SMTP(mail_settings['smtp_server'], mail_settings['smtp_port'])
        mail.ehlo()
        mail.starttls()
        mail.login(mail_settings['smtp_username'], mail_settings['smtp_password'])
        mail.sendmail(email_from, send_to, msg.as_string())
        mail.quit()
        data={"status":1}
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}

    print(print("data++++++++", data))   
    return data

@postpone
def OrderMail(email_to,email_from,email_subject,email_body, bcc=None):
    # email_from == my email address
    # send_to == recipient's email address
    mail_settings = MailSettings()
    email_from = mail_settings['mail_sent_from']
    # email_from = email_from
    send_to = email_to.lower()

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = email_subject
    msg['From'] = email_from
    msg['To'] = send_to
    if bcc is not None and bcc !="":
        msg['Bcc'] = bcc

    # Create the body of the message (a plain-text and an HTML version).
    template = email_body

    # Record the MIME types of both parts - text/plain and text/html.
    # part1 = MIMEText(text, 'plain')
    msg_content = MIMEText(template, 'html')
    msg.attach(msg_content)
    try:
        # Send the message via local SMTP server.
        mail = smtplib.SMTP(mail_settings['smtp_server'], mail_settings['smtp_port'], timeout=20)
        mail.ehlo()
        mail.starttls()
        mail.login(mail_settings['smtp_username'], mail_settings['smtp_password'])
        # mail.sendmail(email_from, send_to, msg.as_string())
        mail.sendmail(email_from, send_to, msg.as_string())
        if bcc is not None and bcc !="":
            mail.sendmail(email_from, bcc, msg.as_string())

        mail.quit()
        data={"status":1}
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
    print("mail data=========", data)
    return data

def SendOtherMail(email_to,email_from,email_subject,email_body):

    mail_settings = MailSettings()
    email_from = mail_settings['mail_sent_from']
    send_to = email_to

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = email_subject
    msg['From'] = email_from
    msg['To'] = send_to
    template = email_body

    # part1 = MIMEText(text, 'plain')
    msg_content = MIMEText(template, 'html')
    msg.attach(msg_content)
    try:
        # Send the message via local SMTP server.
        mail = smtplib.SMTP(mail_settings['smtp_server'], mail_settings['smtp_port'])
        mail.ehlo()
        mail.starttls()
        mail.login(mail_settings['smtp_username'], mail_settings['smtp_password'])
        mail.sendmail(email_from, send_to, msg.as_string())
        mail.quit()
        data={"status":1}
    except Exception as error:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}
    print("data=========", data)
    return data

def SendAllMail(email_to,email_subject,email_body,attachment=None):
    mail_settings = MailSettings()

    email_from  = mail_settings['mail_sent_from']
    send_to     = email_to
    msg             = MIMEMultipart('alternative')
    msg['Subject']  = email_subject
    msg['From']     = email_from
    msg['To']       = send_to

    template    = email_body
    msg_content = MIMEText(template, 'html')
    msg.attach(msg_content)

    #Add attachment
    try:
        if attachment!=None and attachment!="":
            # attach_file_name = attachment
            # attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
            # payload = MIMEBase('application', 'octate-stream')
            # payload.set_payload((attach_file).read())
            # encoders.encode_base64(payload) #encode the attachment
            # #add payload header with filename
            # payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
            # msg.attach(payload)
        
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(attachment,"rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
            msg.attach(part)    
    except:
        pass        


    # Send the message via local SMTP server.
    mail = smtplib.SMTP(mail_settings['smtp_server'], mail_settings['smtp_port'])
    mail.ehlo()
    mail.starttls()
    mail.login(mail_settings['smtp_username'], mail_settings['smtp_password'])
    mail.sendmail(email_from, send_to, msg.as_string())
    mail.quit()
    data={"status":"success"}
    return data

def testmail(email_to, email_subject, email_body):
    mail_settings = MailSettings()

    email_from = mail_settings['mail_sent_from']
    send_to = email_to
    msg = MIMEMultipart('alternative')
    msg['Subject'] = email_subject
    msg['From'] = email_from
    msg['To'] = send_to

    template = email_body
    msg_content = MIMEText(template, 'html')
    msg.attach(msg_content)

    mail = smtplib.SMTP(mail_settings['smtp_server'], mail_settings['smtp_port'])
    mail.ehlo()
    mail.starttls()
    mail.login(mail_settings['smtp_username'], mail_settings['smtp_password'])
    mail.sendmail(email_from, send_to, msg.as_string())
    mail.quit()
    data = {"status": "success"}
    return data
    # SendAllMail(['binayak.santra@navsoft.in'], "Data Pushed to Elastic",
    #                                                       'Data updating to elastic completed', '')


# def CheckTestMail():
#     mail_settings = MailSettings()
#     email_from = mail_settings['mail_sent_from']
#     # email_from = email_from
#     send_to = "kalyanasis.roy@navsoft.in"
#     email_subject = "Test Mail Subject"
#     email_body = "Test mail Body."
#     # Create message container - the correct MIME type is multipart/alternative.
#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = email_subject
#     msg['From'] = email_from
#     msg['To'] = send_to

#     # Create the body of the message (a plain-text and an HTML version).
#     template = email_body

#     # Record the MIME types of both parts - text/plain and text/html.
#     # part1 = MIMEText(text, 'plain')
#     msg_content = MIMEText(template, 'html')
#     msg.attach(msg_content)

#     try:
#         # Send the message via local SMTP server.
#         mail = smtplib.SMTP(mail_settings['smtp_server'], mail_settings['smtp_port'])
#         mail.ehlo()
#         mail.starttls()
#         mail.login(mail_settings['smtp_username'], mail_settings['smtp_password'])
#         mail.sendmail(email_from, send_to, msg.as_string())
#         mail.quit()
#         data={"status":1}
#     except Exception as error:
#         trace_back = sys.exc_info()[2]
#         line = trace_back.tb_lineno
#         data={"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}

#     print(data)
#     return data

# # CheckTestMail()