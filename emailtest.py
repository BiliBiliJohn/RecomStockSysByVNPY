import smtplib
from email.header import Header
from email.mime.text import MIMEText
 
# 第三方 SMTP 服务
mail_host = "smtp.163.com"      # SMTP服务器
mail_user = "*********@163.com"                  # 用户名
mail_pass = "*********"               # 授权密码，非登录密码
 
sender = '*********@163.com'    # 发件人邮箱(最好写全, 不然会失败)
receivers = receivers = ['11111111@qq.com','22222222@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

title = 'Stock trading recommend'  # 邮件主题

def sendEmail(content1,content2):
    mail_html =  '''
        <!DOCTYPE html>
        <html lang="en">
            <head>
            <meta charset="utf-8">
            <STYLE TYPE="text/css" MEDIA=screen>

                table.dataframe {
                    border-collapse: collapse;
                    border: 2px solid #a19da2;
                }

                table.dataframe thead {
                    border: 2px solid #91c6e1;
                    background: #f1f1f1;
                    padding: 10px 10px 10px 10px;
                    color: #333333;
                }

                table.dataframe tbody {
                    border: 2px solid #91c6e1;
                    padding: 10px 10px 10px 10px;
                }

                table.dataframe tr {

                }

                table.dataframe th {
                    vertical-align: top;
                    font-size: 14px;
                    padding: 10px 10px 10px 10px;
                    color: #3da014;
                    font-family: arial;
                    text-align: center;
                }

                table.dataframe td {
                    text-align: center;
                    padding: 10px 10px 10px 10px;
                }

                body {
                    font-family: 宋体;
                }

                h1 {
                    color: #5db446;
                    font-size:15px;
                }

                div.header h2 {
                    color: #3da014;
                    font-family: 黑体;
                }

                div.content h2 {
                    text-align: center;
                    font-size: 10px;
                    text-shadow: 2px 2px 1px #de4040;
                    color: #fff;
                    font-weight: bold;
                    background-color: #008eb7;
                    line-height: 1.5;
                    margin: 20px 0;
                    box-shadow: 10px 10px 5px #888888;
                    border-radius: 5px;
                }

                h3 {
                    font-size: 8px;
                    text-shadow: 2px 2px 1px #de4040;
                    color: #000000;
                    line-height: 1.5;
                }

                h4 {
                    color: #e10092;
                    font-family: 楷体;
                    font-size: 20px;
                    text-align: center;
                }

                td img {
                    max-width: 300px;
                    max-height: 300px;
                }

            </STYLE>
        </head>
        <body>

        <h1><b>
        各位，股市有风险，投资需谨慎！！！
        不对推荐内容负责，仅供参考！！！        
        </b></h1>
        <hr size="1px" noshade=true />
        <p><font color="#0B610B" size="5px"><b>
        特别推荐买入：</b></font></p>
        '''+ content1 +'''
        <p><font color="#0B610B" size="5px"><b>
        推荐卖出：</b></font></p>
        '''+ content2 +'''
        
        <h3><b>
        本邮件由系统自动发出(每天触发)，无需回复！     
        </b></h3>
        </body>
        </html>''' 
    message = MIMEText(mail_html, 'html', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)
 
def send_email2(SMTP_host, from_account, from_passwd, to_account, subject, content):
    email_client = smtplib.SMTP(SMTP_host)
    email_client.login(from_account, from_passwd)
    # create msg
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')  # subject
    msg['From'] = from_account
    msg['To'] = to_account
    email_client.sendmail(from_account, to_account, msg.as_string())
 
    email_client.quit()

# if __name__ == '__main__':
#     sendEmail()
    # receiver = '***'
    # send_email2(mail_host, mail_user, mail_pass, receiver, title, content)
