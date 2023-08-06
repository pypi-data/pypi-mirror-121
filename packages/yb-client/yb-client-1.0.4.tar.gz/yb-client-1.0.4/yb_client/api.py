import requests as request
from yb_client.file import FileManagment

url = 'http://dezh.yottab.io/v1'

def register(user, email, password):
  response = request.post(url + '/user/register?format=json', json={'user': user, 'email':email, 'password':password})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      message = 'Registered successfully.'
    else:
      message = 'Registering Err: %s' % response['msg']
  else:
    message = 'Request Err: %s %s' % (response.status_code, response.reason) 

  return {'type': 'msg', 'msg': message}


def login(user, password):
  message = ''
  response = request.post(url + '/user/token?format=json', json={'user': user, 'password':password})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      fileM  = FileManagment()
      fileM.writeFile(response['data']['value'], user)
      message = 'Logged in successfully.'
    else:
      message = 'Login %s' % response['msg']
  else:
    message = 'Request Err: %s %s' % (response.status_code, response.reason) 

  return {'type': 'msg', 'msg': message}



def logout(token):
  message = ''
  response = request.get(url + '/user/token?format=json', headers={"X-Request-Token": '%s' % token})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      fileM = FileManagment()
      fileM.clearFile()
      message = 'Logged out successfully.'
    else:
      message = 'Logout %s' % response['msg']
  else:
      message='Request Err: %s %s' % (response.status_code, response.reason)
  return {'type': 'msg', 'msg': message}


def createWorkspace(token, user, name, plan):
  response = request.post(url + '/server/action/'+ user + '?format=json', json={'name': name, 'plan':plan}, headers={"X-Request-Token": '%s' % token})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      return {'type': 'table', 'data': [response['data']]}
    else:
      message = 'Creating workspace Err: %s' % response['msg']
      return {'type': 'msg', 'msg': message}
  else:
    message='Request Err: %s %s' % (response.status_code, response.reason)
    return {'type': 'msg', 'msg': message}


def workspaceList(token, user):
  response = request.get(url + '/server/action/'+ user + '?format=json' , headers={"X-Request-Token": '%s' % token})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      return {'type': 'table', 'data': response['data']}
    else:
      message = 'Get workspace list Err: %s' % response['msg']
      return {'type': 'msg', 'msg': message}
  else:
    message='Request Err: %s %s' % (response.status_code, response.reason)
    return {'type': 'msg', 'msg': message}


def mapAppList (apps):
  appList = []
  for app in apps:
    appList.append({'name': app['name'], 'id': app['id']})
  return appList


def workspaceDetail(token, user, workspace):
  wResponse = request.get(url + '/server/action/'+ user + '/' + workspace + '?format=json', headers={"X-Request-Token": '%s' % token})
  if wResponse.status_code == 200:
    aResponse = request.get(url + '/server/apps/'+ user + '/' + workspace + '?format=json', headers={"X-Request-Token": '%s' % token})
    aResponse = aResponse.json()
    appList =  mapAppList(aResponse['data'])
    wResponse = wResponse.json()
    wResponse['data']['apps'] = appList
    if wResponse['code'] == 200:
      return {'type': 'table', 'data': [wResponse['data']]}
    else:
      message = 'Get workspace detail Err: %s' % wResponse['msg']
      return {'type': 'msg', 'msg': message}
  else:
    message='Request Err: %s %s' % (wResponse.status_code, wResponse.reason)
    return {'type': 'msg', 'msg': message}


def restartWorkspace(token, user, workspace):
  message = ''
  response = request.post(url + '/server/restart/'+ user + '/' + workspace + '?format=json', headers={"X-Request-Token": '%s' % token})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      message = 'Workspace restarted successfully.'
    else:
      message = 'Restarting workspace Err: %s' % response['msg']
  else:
      message='Request Err: %s %s' % (response.status_code, response.reason)
  return {'type': 'msg', 'msg': message}


def stopWorkspace(token, user, workspace):
  message = ''
  response = request.post(url + '/server/stop/'+ user + '/' + workspace + '?format=json', headers={"X-Request-Token": '%s' % token})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      message = 'Workspace stopped successfully.'
    else:
      message = 'Stoping workspace Err: %s' % response['msg']
  else:
      message='Request Err: %s %s' % (response.status_code, response.reason)
  return {'type': 'msg', 'msg': message}


def deleteWorkspace(token, user, workspace):  
  message = ''
  response = request.post(url + '/server/delete/'+ user + '/' + workspace + '?format=json', headers={"X-Request-Token": '%s' % token})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      message = 'Workspace deleted successfully.'
    else:
      message = 'Deleting workspace Err: %s' % response['msg']
  else:
      message='Request Err: %s %s' % (response.status_code, response.reason)
  return {'type': 'msg', 'msg': message}


def updateWorkspace(token, user, workspace):
  #response = request.post(url + '/server/setting/'+ user + '/' + workspace + '?format=json', headers={"X-Request-Token": '%s' % token})
  #return response
  pass


def createApp(token, user, workspace, productid, name):
  message = ''
  response = request.post(url + '/server/app_create/'+ user + '/' + workspace + '?format=json', json={'product_id': productid, 'name':name}, headers={"X-Request-Token": '%s' % token})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      message = 'App created successfully.'
    else:
      message = 'Creating app Err: %s' % response['msg']
  else:
      message='Request Err: %s %s' % (response.status_code, response.reason)
  return {'type': 'msg', 'msg': message}


def appList(token, user, workspace):
  response = request.get(url + '/server/apps/'+ user + '/' + workspace + '?format=json', headers={"X-Request-Token": '%s' % token})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      return {'type': 'table', 'data': response['data']}
    else:
      message = 'Get app list Err: %s' % response['msg']
      return {'type': 'msg', 'msg': message}
  else:
    message='Request Err: %s %s' % (response.status_code, response.reason)
    return {'type': 'msg', 'msg': message}


def startApp(token, user, workspace, app_id):
  message = ''
  response = request.post(url + '/server/app_start/'+ user + '/' + workspace + '/' + app_id + '?format=json', headers={"X-Request-Token": '%s' % token})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      message = 'App started successfully.'
    else:
      message = 'Starting app Err: %s' % response['msg']
  else:
      message='Request Err: %s %s' % (response.status_code, response.reason)
  return {'type': 'msg', 'msg': message}


def stopApp(token, user, workspace, app_id):
  message = ''
  response = request.post(url + '/server/app_stop/'+ user + '/' + workspace + '/' + app_id + '?format=json', headers={"X-Request-Token": '%s' % token})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      message = 'App stopped successfully.'
    else:
      message = 'Stoping app Err: %s' % response['msg']
  else:
      message='Request Err: %s %s' % (response.status_code, response.reason)
  return {'type': 'msg', 'msg': message}


def deleteApp(token, user, workspace, app_id):
  message = ''
  response = request.post(url + '/server/app_delete/'+ user + '/' + workspace + '/' + app_id + '?format=json', headers={"X-Request-Token": '%s' % token})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      message = 'App deleted successfully.'
    else:
      message = 'Deleting app Err: %s' % response['msg']
  else:
      message='Request Err: %s %s' % (response.status_code, response.reason)
  return {'type': 'msg', 'msg': message}


def productList(token, user, workspace):
  response = request.get(url + '/server/product/'+ user + '/' + workspace + '?format=json', headers={"X-Request-Token": '%s' % token})
  if response.status_code == 200:
    response = response.json()
    if response['code'] == 200:
      return {'type': 'table', 'data': response['data']}
    else:
      message = 'Get product list Err: %s' % response['msg']
      return {'type': 'msg', 'msg': message}
  else:
    message='Request Err: %s %s' % (response.status_code, response.reason)
    return {'type': 'msg', 'msg': message}

def deleteServer(token, user, workspace):
  #response = request.post(url + '/server/'+ user + '/' + workspace + '?format=json', headers={"X-Request-Token": '%s' % token})
  #return response
  pass
