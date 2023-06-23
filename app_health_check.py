import requests
import smtplib
import os
#for ssh
import paramiko

#~/.bash_profile
#EMAIL_ADDRESS="test@gmail.com"
#EMAIL_PASSWORD="<<PASSWORD>>"

email_addr = os.environ.get('EMAIL_ADDRESS')
email_pw = os.environ.get('EMAIL_PASSWORD')

def send_notification(email_msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        # use two step authentication and gmail "app passwords", not your own
        smtp.login(email_addr, email_pw)
        message = f"Subject: SITE DOWN\n{email_msg}"
        smtp.sendmail(email_addr, email_addr, message)


def restart_container():
    ssh = paramiko.SSHClient()
    # say yes to host key check
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect('132.132.122.223', 22, 'admin', key_filename='/home/admin/is_rsa')
    stdin, stdout, stderr = ssh.exec_command('docker restart xxxxxx')
    print(stdout.readlines())
    ssh.close()
    print('Container Restarted')


def monitor_application():
    try:
        response = requests.get('http://google.com/')

        if response.status_code == 200:
            print('Application is running successfully!')
        else:
            print('Application Down.')
            msg = f"Application returned {response.status_code}."
            send_notification(msg)
            # restart the application
            restart_container()
    except Exception as ex:
        print(f'Something went wrong, looks like its {ex}. I will send an e-mail..')
        msg = 'Application Service not responding.'
        send_notification(msg)

