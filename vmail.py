import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

session = smtplib.SMTP("smtp.webfaction.com",25)
session.set_debuglevel(1)
session.starttls
session.login("edciitr","edciitrnumber1")

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
# Create a text/plain message
msg = MIMEText("Hi Group, <br/>This is a test message. If you are seeing a well formatted version of this message on the group, the test has succeeded. <hr /><span style='color:grey'>Please ignore this message. And if you are really frustrated with all these messages please delete them.  <br />Thanks and regards,<br />Vikesh</span>",'html')
me = "feedback@edciitr.com"
you = "edciitr@googlegroups.com"
# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = "[Feedback] Testing"
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
session.sendmail(me, [you], msg.as_string())
session.quit()

