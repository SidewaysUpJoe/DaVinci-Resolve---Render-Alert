# DaVinci Resolve - Render Alert
This script will and send off an email(s) (and text messages) through your gmail account when your render finishs with information about the render. For windows users you can also have the script 'beep' when render is finished. The script can be run two different ways: as a "stand alone" script or from Davinci's script menu.

For running through Davinci, you will have to save the script to Davinci's ...\Scripts\Deliver\ dir.


**Windows path:** C:\ProgramData\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Deliver

**MAC path:** /Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver

**Linux path:** /opt/resolve/Fusion/Scripts (or /home/resolve/Fusion/Scripts/Deliver depending on installation)

The script was tested with Davinci Resolve 18, but do not see any reason why it will not work with earlyer version.

* Heres a **video of a full howto** for using the script https://youtu.be/gW3vY_qDD_I



Example of what the email (or sms) will look like. All info is being pulled from Davinci.

Email Subject Title will be:
```
Davinci Render: Your Project's Name
```



Email Body
```
Start:          05/15/2022, 06:28:15 PM
Finished:       05/15/2022, 06:28:33 PM
Total:          0:00:17

Job 1
Timeline:      SECOND TIMELINE
Save Path:     C:\Users\Joe\Desktop\delete.me.mov
Job Status:    Complete
Completion:    %100
Render Time:   00:00:04

NEW JOB NAME
Timeline:      Timeline 1
Save Path:     C:\Users\Joe\Desktop\delete.me2.mov
Job Status:    Complete
Completion:    %100
Render Time:   00:00:11


PC:             COMPUTER NAME
USER:           Joe
Davinci Ver:    18.0.0b.7
```

## Configuration
There are acouple things which you will have to edit.


### Library Path
Depending on the Operating System you are using you will have to pick the 'lib_' path:

All paths supplied in the script are standard paths from Davinci's scripting readme file.

Path varibules are:
* lib_mac
* lib_win
* lib_linux

```
dvr_script = imp.load_dynamic('fusionscript', lib_win)
```



### Email
Need to config your email information
```
emailVar = {
    'gmail_userName': 'your@gmail.com', # HERE
    'gmail_password': 'abc123', # HERE - You can try your email password, but your probly gonna need an Gmail APP password. Its free and easy. https://www.google.com/search?q=python+gmail+smtp+app+password
    'smtp_addy': 'smtp.gmail.com',
    'smtp_port': 465,
    'mailTo': ['sendTo@email.com', '1234567890@vzwpix.com'], # HERE
    'subject_pre': 'Davinci Render: ' # HERE
        }

```


### Beep
For windows uses who want the script to beep when render finishs:
You will need to change this to True
```
makeBeep = False # for Windows: used at bottom of script
```
