#!/usr/bin/env python

import os
import socket
import time
import imp
import smtplib
from datetime import datetime


lib_mac = '/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so'
lib_win = 'C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscript.dll'
lib_linux = '/opt/resolve/libs/Fusion/fusionscript.so'


# EDIT **
dvr_script = imp.load_dynamic('fusionscript', lib_win)  # SELECT: lib_mac OR lib_win OR lib_linux OR your own custom path if needed

# EDIT **
makeBeep = False # for Windows users: True or False

# EDIT **
emailVar = {
    'gmail_userName': 'your@gmail.com', # HERE
    'gmail_password': 'abc123', # HERE - You can try your email password, but your probly gonna need an Gmail APP password. Its free and easy. https://www.google.com/search?q=python+gmail+smtp+app+password
    'smtp_addy': 'smtp.gmail.com',
    'smtp_port': 465,
    'mailTo': ['sendTo@email.com', '1234567890@vzwpix.com'], # HERE
    'subject_pre': 'Davinci Render: ' # HERE
        }


# LANG
suj_Lang = {
    'ErrEmail_UsrPwd': 'ERROR: Email did not send... \n\rBad Username or Password',
    'ErrEmail_SMTP': 'ERROR: Email did not send... \n\rWrong SMTP address or SMTP port',
    'ErrEmail_MISC': 'Email: Something went wrong, Email did not send...\n\r Sento address wrong or error with-in body of email...' 
    }


# Create the instances you need...
resolve = dvr_script.scriptapp('Resolve')
#fusion   = dvr_script.scriptapp('Fusion')

projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()


_RENDER_START_TIME = None
pcName = socket.gethostname()
userName = os.environ.get('USERNAME')
dvrVer = resolve.GetVersionString()



def IsRenderingInProgress( resolve ):
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    if not project:
        return False

    return project.IsRenderingInProgress()

def WaitForRenderingCompletion( resolve ):
    while IsRenderingInProgress(resolve):
        time.sleep(1)
    return




def sendEmail(message):

    subject = emailVar['subject_pre'] + project.GetName()
    
    try:
        s = smtplib.SMTP_SSL(emailVar['smtp_addy'], emailVar['smtp_port'])
        s.ehlo()
    except Exception as e:
        print(suj_Lang['ErrEmail_SMTP'])
        s.quit()
        return
    
    try:
        s.login(emailVar['gmail_userName'], emailVar['gmail_password'])
    except Exception as e:
        print(suj_Lang['ErrEmail_UsrPwd'])
        s.quit()
        return

    email_text = """\
Subject: %s

Start:             %s
Finished:       %s
Total:             %s

%s
PC:                     %s
USER:               %s
Davinci Ver:    %s
""" % (subject, start_time, end_time, t_time, message, pcName, userName, dvrVer)
 
    try:
        s.sendmail(emailVar['gmail_userName'], emailVar['mailTo'], email_text)
    except Exception as e:
        print(suj_Lang['ErrEmail_MISC'])
        
    s.quit()



_RENDER_START_TIME = datetime.now()

#project.SaveProject()
project.StartRendering()
WaitForRenderingCompletion(resolve)


msg = ''
timeLines = project.GetRenderJobs()

# {'JobId': '1836d290-bcb8-45aa-b928-b748a67b172a'
# RenderJobName': 'Job 1'
# TimelineName': 'SECOND TIMELINE'
# TargetDir': 'C:\\Users\\Joe\\Desktop'
# IsExportVideo': True
# IsExportAudio': True
# FormatWidth': 1920
# FormatHeight': 1080
# FrameRate': '23.976'
# PixelAspectRatio': 1.0
# MarkIn': 86400
# MarkOut': 87667
# AudioBitDepth': 16
# AudioSampleRate': 48000
# ExportAlpha': False
# OutputFilename': 'delete.me.mov'
# RenderMode': 'Single clip'
# PresetName': 'Custom'
# VideoFormat': 'QuickTime'
# VideoCodec': 'H.264 NVIDIA'
# AudioCodec': 'lpcm'
# EncodingProfile': ''
# MultiPassEncode': False
# NetworkOptimization': False}


for id in timeLines:
    tLineID = project.GetRenderJobs()[id]['JobId']

    timelineTXT = ''
    timelineTXT = timelineTXT + project.GetRenderJobs()[id]['RenderJobName']  + "\n"
    timelineTXT = timelineTXT + "Timeline:          " + project.GetRenderJobs()[id]['TimelineName']  + "\n"
    timelineTXT = timelineTXT + "Save Path:         " + project.GetRenderJobs()[id]['TargetDir']  + "\\" + project.GetRenderJobs()[id]['OutputFilename']  + "\n"
    
    timelineTXT = timelineTXT + "Job Status:        " + project.GetRenderJobStatus(tLineID)['JobStatus'] + "\n"
    timelineTXT = timelineTXT + "Completion:     %" + str(project.GetRenderJobStatus(tLineID)['CompletionPercentage']) + "\n"
    
    if 'TimeTakenToRenderInMs' in project.GetRenderJobStatus(tLineID):
        TimeTakenToRenderInMs = project.GetRenderJobStatus(tLineID)['TimeTakenToRenderInMs']
        seconds=(TimeTakenToRenderInMs/1000)%60
        seconds = int(seconds)
        minutes=(TimeTakenToRenderInMs/(1000*60))%60
        minutes = int(minutes)
        hours=(TimeTakenToRenderInMs/(1000*60*60))%24

        lineRT = "%02d:%02d:%02d" % (hours, minutes, seconds)
        timelineTXT = timelineTXT + "Render Time:   " + lineRT + "\n"

    msg = msg + timelineTXT  + "\n"




now = datetime.now()
start_time = _RENDER_START_TIME.strftime("%m/%d/%Y, %I:%M:%S %p")
end_time = now.strftime("%m/%d/%Y, %I:%M:%S %p")
t_time = now - _RENDER_START_TIME
t_time=str(t_time).split('.', 2)[0]

if makeBeep == True:
    import winsound
    frequency = 1000
    duration = 1250
    winsound.Beep(frequency, duration)

sendEmail(msg)
print("Rendering is completed.")

