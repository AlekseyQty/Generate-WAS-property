from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from file_operations import *
import os.path
import os

#Constants
DEFAULTWITDTH = 40
CLUSTERWIDTH  = 50
filename = ''

#Root options
root = Tk()
root.title('Generate config')
root.resizable(width=False,height=False)
# root.geometry('{}x{}'.format(800, 600))
root.style = ttk.Style()
root.style.configure('TButton',background = 'green')

#Functions
def getContentFromFile(filename):
    with open(filename) as f:
        lines = f.readlines()
    content = [x.strip() for x in lines]
    return content

def getValuesFromCallbacks():
    spheres = getContentFromFile(filename)

    newApps = [appNewListbox.get(i) for i in appNewListbox.curselection()]
    oldApps = [appOldListbox.get(i) for i in appOldListbox.curselection()]
    newClusters = [clusterNewList.get(i) for i in clusterNewList.curselection()]
    oldClusters = [clusterOldList.get(i) for i in clusterOldList.curselection()]
    nodeNew = box_value_new.get()
    nodeOld = box_value_old.get()
    callbackDict = {'spheres':spheres,'newApps':newApps,'oldApps':oldApps,'newClusters':newClusters,'oldClusters':oldClusters,
                    'nodeNew':nodeNew,'nodeOld':nodeOld}
    return callbackDict

#Functions for error handling
def isCheckedNew():
    resultDict = getValuesFromCallbacks()
    if box_value_new.get()!='' or resultDict['newClusters'] or resultDict['newApps']:
        return True
    else:
        return False

def isAllAcheckedNew():
    resultDict = getValuesFromCallbacks()
    if box_value_new.get()!='' and resultDict['newClusters'] and resultDict['newApps']:
        return True
    else:
        return False

def isCheckedOld():
    resultDict = getValuesFromCallbacks()
    if box_value_old.get()!='' or resultDict['oldClusters'] or resultDict['oldApps']:
        return True
    else:
        return False

def isAllAcheckedOld():
    resultDict = getValuesFromCallbacks()
    if box_value_old.get()!='' and resultDict['oldClusters'] and resultDict['oldApps']:
        return True
    else:
        return False

def generateFinalresult():
    resultDict = getValuesFromCallbacks()
    generateResult(resultDict['spheres'], resultDict['newApps'], resultDict['oldApps']
                   , resultDict['newClusters'], resultDict['oldClusters'],
                   resultDict['nodeNew'], resultDict['nodeOld'])
    messagebox.showinfo("Done", "Files generated")

#Callback functions
def nodeNewButtonCallback():
    if (os.path.isfile(filename) == False):
        messagebox.showinfo("Error opening file", "choose a file!")
    else:
        resultDict = getValuesFromCallbacks()
    if isCheckedNew() and isCheckedOld():
        if isAllAcheckedNew() and isAllAcheckedOld():
            generateFinalresult()
        else:
            messagebox.showinfo("Error", "Select all fields")
    if isCheckedNew() and not isCheckedOld():
        if isAllAcheckedNew():
            generateFinalresult()
        else:
            messagebox.showinfo("Error", "Select all fields for new apps")
    if isCheckedOld() and not isCheckedNew():
        if isAllAcheckedOld():
            generateFinalresult()
        else:
            messagebox.showinfo("Error", "Select all fields for old apps")

def fileOpenCallback():
    global filename
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                   filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
def hideCallback():
    nodeNewButtonTest.grid_forget()
    nodeNewText.grid_forget()
    nodeNewCombobox.grid_forget()

def testClick():
    treeView.insert(newApps, 'end', 'App1', text='Sub app1', values=('+', '+', '', ''))

selectedNewApps = {}
selectedOldApps = {}

def generateTreeOptions(): #TODO DOPILIT
    for app in selectedNewApps:
        for clu in selectedNewApps[app]:
            clusterList = []
            # print(clu)
            if clu == 'ERIB_Clu1':
                clusterList.append('+')
            else:
                clusterList.append('-')
            if clu == 'ERIB_Clu2':
                clusterList.append('+')
            else:
                clusterList.append('-')
            if clu == 'ERIB_Clu3':
                clusterList.append('+')
            else:
                clusterList.append('-')
            if clu == 'ERIB_Clu4':
                clusterList.append('+')
            else:
                clusterList.append('-')
            clusterTuple = tuple(clusterList)
            print(clusterTuple)
        treeView.insert(newApps, 'end', app, text=app, values=clusterTuple)

def generateSelected():
    # global selectedNewApps

    newClusters = [clusterNewList.get(i) for i in clusterNewList.curselection()]
    oldClusters = [clusterOldList.get(i) for i in clusterOldList.curselection()]
    for app in [appNewListbox.get(i) for i in appNewListbox.curselection()]:
        selectedNewApps[app] = newClusters
    for app in [appOldListbox.get(i) for i in appOldListbox.curselection()]:
        selectedOldApps[app] = oldClusters
    for cnt,i in enumerate(appNewListbox.curselection()):
        # print("Deleting " + appNewListbox.get(i-cnt) + ' index ' + str(i-cnt) + " cnt " + str(cnt))
        appNewListbox.selection_clear(i-cnt)
        appNewListbox.delete(i-cnt)
    for cnt,i in enumerate(appOldListbox.curselection()):
        # print("Deleting " + appNewListbox.get(i-cnt) + ' index ' + str(i-cnt) + " cnt " + str(cnt))
        appOldListbox.selection_clear(i-cnt)
        appOldListbox.delete(i-cnt)

def newGenerateResult():
    spheres = getContentFromFile(filename)
    # newApps = [appNewListbox.get(i) for i in appNewListbox.curselection()]
    # oldApps = [appOldListbox.get(i) for i in appOldListbox.curselection()]
    # newClusters = [clusterNewList.get(i) for i in clusterNewList.curselection()]
    # oldClusters = [clusterOldList.get(i) for i in clusterOldList.curselection()]
    nodeNew = box_value_new.get()
    nodeOld = box_value_old.get()
    generateResult(spheres, selectedNewApps, selectedOldApps
                   ,nodeNew, nodeOld)
    messagebox.showinfo("Done", "Files generated")

def updateCallback():
    generateSelected()
    generateTreeOptions()
    print(selectedNewApps)

#Labels
nodeNewText = Label(root,text = 'Select new node: ')
nodeNewText.grid(row=0)

nodeOldText = Label(root,text = 'Select old node: ')
nodeOldText.grid(row=0,column=1)

appNewText = Label(root,text = 'Select new apps: ')
appNewText.grid(row=2)

appNewText = Label(root,text = 'Select old apps: ')
appNewText.grid(row=2,column = 1)

nodeNewText = Label(root,text = 'Select new clusters: ')
nodeNewText.grid(row=4)

nodeNewText = Label(root,text = 'Select old clusters: ')
nodeNewText.grid(row=4,column = 1)

#Comboboxes
box_value_new = StringVar()
boxValuesNew = nodeList
nodeNewCombobox = ttk.Combobox(root, textvariable=box_value_new, values = boxValuesNew, width =DEFAULTWITDTH - 5, state ='readonly')
nodeNewCombobox.grid(row=1)

box_value_old = StringVar()
boxValuesOld = nodeList
nodeOldCombobox = ttk.Combobox(root, textvariable=box_value_old, values = boxValuesOld, width =DEFAULTWITDTH - 5, state ='readonly')
nodeOldCombobox.grid(row=1,column=1)

#Buttons
nodeNewButton = ttk.Button(root,text = 'Confirm',command = newGenerateResult,width = DEFAULTWITDTH*2)
nodeNewButton.grid(row=7,columnspan = 2)

# nodeNewButtonTest = ttk.Button(root,text = 'Select more',command = updateCallback,width = DEFAULTWITDTH*2)
# nodeNewButtonTest.grid(row=8,columnspan = 2)

nodeNewButtonTest = ttk.Button(root,text = 'Select more',command = updateCallback,width = DEFAULTWITDTH*2)
nodeNewButtonTest.grid(row=8,columnspan = 2)

nodeNewButtonSphere = ttk.Button(root,text = 'Choose web spheres',command = fileOpenCallback,width = DEFAULTWITDTH*2)
nodeNewButtonSphere.grid(row=6,columnspan = 2)

#Treeview
treeView = ttk.Treeview()
treeView['columns'] = ('Clu1','Clu2','Clu3','Clu4')
treeView.column('Clu1',width = CLUSTERWIDTH)
treeView.column('Clu2',width = CLUSTERWIDTH)
treeView.column('Clu3',width = CLUSTERWIDTH)
treeView.column('Clu4',width = CLUSTERWIDTH)
treeView.heading('Clu1',text = 'Clu1')
treeView.heading('Clu2',text = 'Clu2')
treeView.heading('Clu3',text = 'Clu3')
treeView.heading('Clu4',text = 'Clu4')
newApps = treeView.insert('',0,'newApps',text = 'New apps')
oldApps = treeView.insert('',1,'oldApps',text = 'Old apps')

treeView.grid(row = 3,column =2,sticky = 'N')

#Listboxes
appList = generateAppNamesList() #All apps to chose from

appNewListbox = Listbox(root,selectmode = 'multiple',width = DEFAULTWITDTH-2,exportselection = False,height = 40)
for i,app in enumerate(appList):
    appNewListbox.insert(i,app)
appNewListbox.grid(row=3)

appOldListbox = Listbox(root,selectmode = 'multiple',width = DEFAULTWITDTH-2,exportselection = False,height = 40)
for i,app in enumerate(appList):
    appOldListbox.insert(i,app)
appOldListbox.grid(row=3,column = 1)

clusterNewList = Listbox(root, selectmode ='multiple', width =DEFAULTWITDTH - 2, exportselection = False, height = 4)
for i,cluster in enumerate(clusterList):
    clusterNewList.insert(i, cluster)
clusterNewList.grid(row=5)

clusterOldList = Listbox(root, selectmode ='multiple', width =DEFAULTWITDTH - 2, exportselection = False, height = 4)
for i,cluster in enumerate(clusterList):
    clusterOldList.insert(i, cluster)
clusterOldList.grid(row=5,column = 1)

root.mainloop()

#TODO Property edit