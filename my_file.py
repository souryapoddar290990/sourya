# import smtplib
# msg = "TESTING"
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.ehlo()
# server.starttls()
# server.ehlo()
# server.login("souryapoddar290990@gmail.com", "souryaindia")
# server.sendmail("souryapoddar290990@gmail.com", ["aryapoddar290990@gmail.com"], msg)
# server.quit()

# import smtplib
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
# from email.MIMEBase import MIMEBase
# from email import encoders
# fromaddr = 'souryapoddar290990@gmail.com'
# toaddr = ["aryapoddar290990@gmail.com","souryapoddar290990@gmail.com"]
# password = "souryaindia"
# subject = "SUBJECT OF THE EMAIL"
# filename = "HYD-HWH.pdf"
# path = 'C:/Users/DELL/Downloads/'
# body = "TEXT YOU WANT TO SEND"
# msg = MIMEMultipart()
# msg['From'] = fromaddr
# msg['To'] = ",".join(toaddr)
# msg['Subject'] = subject
# msg.attach(MIMEText(body, 'plain'))
# attachment = open(path+filename, "rb")
# part = MIMEBase('application', 'octet-stream')
# part.set_payload((attachment).read())
# encoders.encode_base64(part)
# part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
# msg.attach(part)
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login(fromaddr,password)
# text = msg.as_string()
# server.sendmail(fromaddr, toaddr, text)
# server.quit()