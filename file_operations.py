from app_list import *
import os

def generateAppNamesList():
    appNameList = []
    for app in appDict:
        appNameList.append(app)
    return appNameList

def generateAppName(appname,node):
    if (appDict[appname][1]==False):
        return appname
    else:
        return (str(appname)+'_'+ str(node))

def generateString(source):
    string = ''
    for r in source:
        string+=str(r)
        if (r!=source[-1]):
            string+=','
    return string

#Generate string like map.servers.list.phizic_atm_node0 = WebSphere:cell=V-ERIB-8R2-2011Cell01,cluster=ERIB_Clu1+WebSphere:
# cell=V-ERIB-8R2-2011Cell01,cluster=ERIB_Clu2+WebSphere:cell=V-ERIB-8R2-2011Cell01,cluster=ERIB_Clu3+WebSphere:
# cell=V-ERIB-8R2-2011Cell01,cluster=ERIB_Clu4
def generateWebsphereString(app,sphere,clusters):
    string = 'map.servers.list.' + app + ' = '
    for clu in clusters:
        string += 'WebSphere:cell=' + sphere + 'Cell01,cluster='+clu
        if (clu!=clusters[-1]):
            string+='+'
    return string


def generateResult(sphereList,newApps,oldApps,newNode,oldNode):
    # newApps = [appNewListbox.get(i) for i in appNewListbox.curselection()]
    newAppsWithNodes = [generateAppName(i,newNode) for i in newApps.keys()]
    oldAppsWithNodes = [generateAppName(i,oldNode) for i in oldApps.keys()]
    newAppsString = generateString(newAppsWithNodes)
    oldAppsString = generateString(oldAppsWithNodes)
    if sphereList:
        if not os.path.exists('Result/'):
            os.makedirs('Result/')
    for sphere in sphereList:
        with open('Result/' + str(sphere), 'w') as the_file:
            the_file.write(
                '#-\n'
                'was.phizic.apps = ' + newAppsString + '\n' +
                'was.phizic.oldapps = ' + oldAppsString + '\n'
            )
            for app in newApps.keys():
                appWithNode = generateAppName(app,newNode)
                additionalString = (60 - int(len(appWithNode))) * "-"
                the_file.write(
                    '#--- ' + appWithNode + ' ' + additionalString + '\n'
                )
                the_file.write(
                    generateWebsphereString(appWithNode,sphere,newApps[app]) + '\n'
                )
                the_file.write(
                    'map.modules.to.servers.' + appWithNode + ' = ' + appDict[app][0]+ '\n'
                )
            for app in oldApps.keys():
                appWithNode = generateAppName(app,oldNode)
                additionalString = (60 - int(len(appWithNode))) * "-"
                the_file.write(
                    '#--- ' + appWithNode + ' ' + additionalString + '\n'
                )
                the_file.write(
                    generateWebsphereString(appWithNode,sphere,oldApps[app]) + '\n'
                )
                the_file.write(
                    'map.modules.to.servers.' + appWithNode + ' = ' + appDict[app][0]+ '\n'
                )