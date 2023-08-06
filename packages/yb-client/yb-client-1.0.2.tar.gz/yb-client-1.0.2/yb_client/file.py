import os


class FileManagment:
  def __init__(self):
    try:
      file=open('config.txt', 'x')
      file.close()
    except:
      pass

  def writeFile(self, token, user):
    file=open('config.txt', 'w')
    file.write("")
    file.write("token='%s' \nuser='%s'" % (token, user))
    file.close()
    return 'successful writing'

  def clearFile(self):
    file=open('config.txt', 'w')
    file.write("")
    file.close()
    return 'successful clearing'

  def readFile(self):
    if os.path.getsize('config.txt') != 0 :
      file = open('config.txt', 'r')
      firstLine = file.readline().rsplit('=')[1]
      user = file.readline().rsplit('=')[1]
      token =firstLine.rsplit('\n')[0]
      token = token.rsplit('\'')[1]
      user = user.rsplit('\'')[1]
      file.close()
    else:
      token = None
      user = None    
    return {'token':token, 'user':user}
