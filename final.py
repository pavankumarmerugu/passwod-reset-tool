from flask import render_template
from flask import Flask, flash, request, redirect
import paramiko
import re


#p = paramiko.SSHClient()
#p.set_missing_host_key_policy(
#    paramiko.AutoAddPolicy())  # This script doesn't work for me unless this line is added!
#p.connect("172.23.254.117", port=22, username="testuser1", password="123Omni:us")


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
sshipaddr = ""
sshport = 22
sshuname = "your username"
sshpassword = "your password"

message = ""
flag = 0
@app.route('/')

def home():
    return render_template('password.html')

@app.route('/password', methods=['POST', 'GET'])
def password():
    if request.method == 'POST':
        user = request.form['uname']
        oldpassword = request.form['oldpassword']
        newpassword = request.form['newpassword']
        confirmnewpassword = request.form['confirmnewpassword']
        #if user == 'pavan':
        #    return render_template('changepassword.html')
        #else:
        #    return 'you failed'



        #oldpassword = input("Enter old password:")
        #newpassword = input("Enter new password:")

        # stdin, stdout, stderr = p.exec_command('ipconfig')
        if newpassword == confirmnewpassword:
            print('Password matches')

            while True:
                if (len(newpassword) < 8):
                    flag = -1
                    break
                elif not re.search("[a-z]", newpassword):
                    flag = -1
                    break
                elif not re.search("[A-Z]", newpassword):
                    flag = -1
                    break
                elif not re.search("[0-9]", newpassword):
                    flag = -1
                    break
                elif not re.search("[!&/?%:_@$]", newpassword):
                    flag = -1
                    break
                elif re.search("\s", newpassword):
                    flag = -1
                    break
                else:
                    flag = 0
                    print("Valid new Password")

                    try:
                        p = paramiko.SSHClient()
                        p.set_missing_host_key_policy(
                            paramiko.AutoAddPolicy())  # This script doesn't work for me unless this line is added!
                        p.connect(sshipaddr, sshport, username=sshuname, password=sshpassword)
                        print('connected')
                    except paramiko.AuthenticationException:
                        print('Failed to connect to %s due to wrong username/password')
                        exit(1)
                    except Exception as e:
                        print(e.message)
                        exit(2)


                    stdin, stdout, stderr = p.exec_command("Set-AdAccountPassword -Identity " + user + " -OldPassword "
                                            "(ConvertTo-SecureString -AsPlainText"
                                            " " + oldpassword + " -Force) -NewPassword (ConvertTo-SecureString "
                                            "-AsPlainText " + newpassword + " -Force)")

                    err = stderr.readlines()
                    opt = stdout.readlines()
                    err = "".join(err)
                    opt = "".join(opt)
                    print(err)
                    print(user)
                    p.close()
                    break
                    #global message
            message = "Password changed successfully"

            if flag == -1:
                print("Not a Valid Password")
                message = "not a valid password.check the password policy mentioned here"
        else:
            print('old and new passwords do not match')
            #global message
            message = "passwords do not match"

    print(message)
    flash(message)
    return render_template('password.html')

    #return render_template('userform.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')