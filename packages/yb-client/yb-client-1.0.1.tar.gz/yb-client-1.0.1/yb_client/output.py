from tabulate import tabulate

def register(output):
  return output['msg']

def login(output):
  return output['msg']

def logout(output):
  return output['msg']

def createWorkspace(output):
  if output['type'] == 'table':
    table = []
    headers = ['name', 'state', 'plan']
    for workspace in output['data']:
      table.append([workspace['name'], workspace['state'], workspace['plan']])
    return tabulate(table, headers=headers, tablefmt="pretty")
  else:
    return output['msg']

def workspaceList(output):
  if output['type'] == 'table':
    table = []
    headers = ['name', 'state', 'plan']
    for workspace in output['data']:
      table.append([workspace['name'], workspace['state'], workspace['plan']])
    return tabulate(table, headers=headers, tablefmt="pretty")
  else:
    return output['msg']

def workspaceDetail(output):
  i = 0
  if output['type'] == 'table':
    wTable = []
    aTable = []
    wHeaders = ['worskspace_name', 'state', 'plan', 'app_name', 'app_id']
    aHeaders = ['app_name', 'id']
    for workspace in output['data']:
      for app in workspace['apps']:
        if i == 0:
          i += 1
          wTable.append([ workspace['name'], workspace['state'], workspace['plan'],app['name'], app['id']])
        else:
          wTable.append(["-", "-", "-",app['name'], app['id']])
    wTable = tabulate(wTable, headers=wHeaders, tablefmt="pretty")
    return wTable
  else:
    return output['msg']

def restartWorkspace(output):
  return output['msg']

def stopWorkspace(output):  
  return output['msg']
  pass

def deleteWorkspace(output): 
  return output['msg']

def updateWorkspace():
  pass

def createApp(output):
  return output['msg']

def appList(output):
  if(output['type'] == 'table'):
    message = ''
    headTable = []
    headHeaders = ['name', 'state', 'app_id', 'product_id']
    for app in output['data']:
      headTable.append([app['name'], app['state'], app['id'], app['product_id']])
    return tabulate(headTable, headers=headHeaders, tablefmt="pretty", colalign=("left", "left", "left", "left"))
  else:
    return output['msg']
  
def startApp(output):
  return output['msg']

def stopApp(output):
  return output['msg']

def deleteApp(output):
  return output['msg']

def deleteServer():
  pass

def productList(output):
  if(output['type'] == 'table'):
    headTable = []
    headHeaders = ['name', 'product_id', 'type']
    for app in output['data']:
      headTable.append([app['name'], app['id'], app['type']])
    return tabulate(headTable, headers=headHeaders, tablefmt="pretty", colalign=("left","left", "left",))
  else:
    return output['msg']