# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 18:12:41 2024

@author: eng alaa khalid
"""
import time
import re
from getpass import getpass
import json
login_user={}
users_list=[]
user={}
projects_list=[]
f_name,l_name,email,password,confirmPasswoed,mobile="","","","","",""
project={}
title,details="",""
totalTarget,year,month,day=0,0,0,0

 


def read_users_json(file):
    try:
        users_file=open(file)
        data=json.load(users_file)
    except Exception as s:
        return None
    else:
        print(data)
        return data

def pushToFile(user:dict):
    users_list=read_users_json("users.json")
    users_list.append(user)
    
    try:
        users_file=open("users.json","w")
    except Exception as s:
            print(f"problem in users json file {s}")
    else:
        json.dump(users_list,users_file , indent=4)
        print(users_list)
        return True
           

def getPasswordData(sentence:str):
    password=getpass(f"{sentence}\n")
    while not re.match("^[a-zA-Z]*[0-9]*$",password):
        print("invalid password syntax\n")
        password=getpass(f"{sentence}\n")
    return password



def getStrData(sentence:str):
    name=input(f"{sentence}\n")
    while name.isnumeric() or not re.match("^[a-zA-Z ]*$",name):
        print("invalid naming syntax\n")
        name=input(f"{sentence}\n")
    return name


def emailValidation(sentence:str):
    email=input(f"{sentence}\n")
    while not re.fullmatch("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",email):
        print("invalid email\n")
        email=input(f"{sentence}\n")
    return email
    
def phoneValidation(sentence:str):
    phone=input(f"{sentence}\n")
    while phone.isalpha() or not re.match("^[0][1][0125][0-9]{8}$",phone):
        print("invalid phone number\n")
        phone=input(f"{sentence}\n")
    return phone


def userIsExist(check_user):
    listOfUsers=read_users_json("users.json")
    for user in listOfUsers:
        if check_user["email"]==user["email"]:
            if user["password"]!=check_user["password"]:
                password=input("please enter your password\n")
            print("=============account is exist============")
            return True
    goToRegister=input("no such an account. go to register?[y/n]\n")
    if goToRegister=="y":
        register()
    else:
        return False

def projectDel(project_title):
    listOfProjects=read_users_json("projects.json")
    if not listOfProjects:
        goToMenu=input("no such a project. go to menu?[y/n]\n")
        if goToMenu=="y":
            projectMenu()
        else:
             return False
    for project in range(len(listOfProjects)):
        if project_title==listOfProjects[project]['title']:
            print("=============project is exist============")
            if listOfProjects[project]['login_user']!=login_user:
                print("=============owner only can delete project============")
            else:
                print("=====project will be deleted=========")
                print("project title:",listOfProjects[project]["title"],"\nproject detail:",listOfProjects[project]["details"],"project total target:",listOfProjects[project]["totalTarget"],"\nproject owner:",listOfProjects[project]['login_user'])
                del listOfProjects[project]
                print(listOfProjects)
                projects_file=open("projects.json","w")
                json.dump(listOfProjects,projects_file, indent=4)
                projects_file.close()
                print("============project deleted successfully=========")
                projectMenu()
    goToMenu=input("no such a project. go to menu?[y/n]\n")
    if goToMenu=="y":
        projectMenu()
    else:
        return False

def checkDate(time_data,dateFormat):
    try:
        date=time.strptime(time_data,dateFormat)
        print(date)
        return date
    except Exception as s:
        print(s)
        return False
    
def createProject():
    title=getStrData("enter project title\n")
    details=getStrData("enter project details\n")
    totalTarget=input("enter project total target\n")
    while not totalTarget.isnumeric():
        print("total target must be a number\n")
        totalTarget=input("enter project total target\n")
    startDate=input("please enter start data in the following format \'day-month-years\'\n")
    while not checkDate(startDate,"%d-%m-%Y"):
        startDate=input("please enter valid data in the following format \'day-month-years\'\n")
    endDate=input("please enter end data in the following format \'day-month-years\'\n")
    while not checkDate(endDate,"%d-%m-%Y"):
        endDate=input("please enter valid data in the following format \'day-month-years\'\n")
    while checkDate(endDate,"%d-%m-%Y").tm_year<checkDate(startDate,"%d-%m-%Y").tm_year:
        endDate=input("please enter valid end data\n")
    print(login_user)    
    project={"title":title,"details":details,"totalTarget":totalTarget,"startDate":startDate,"endDate":endDate,"login_user":login_user}
    try:
        projects_list=read_users_json("projects.json")
        projects_list.append(project)
    except :
        projects_list=[]
        projects_list.append(project)
    projects_file=open("projects.json","w")
    print(projects_list)
    json.dump(projects_list,projects_file, indent=4)
    print("=====project added successfully========")
    projects_file.close()
    projectMenu()
    
def listProjects():
    try:
        projects_file=open("projects.json","r")
        projects_list=json.load(projects_file)
        for project in projects_list:
            print("project title:",project["title"],"\nproject detail:",project["details"],"project total target:",project["totalTarget"],"\nproject owner:",project['login_user'])
            print("===================================================================")
    except Exception as s:
        print("======no projects found=========\n",s)
    projectMenu()
    
    
    
def projectMenu():
    option=input("enter\n1 for projects list\n2 for edit Project\n3 for delete project\n4 for create project\n")
    while not option.isnumeric() or int(option) not in (1,2,3,4):
        print("invalid selection")
        option=input("1 for projects list\n2 for edit Project\n3 for delete project\n4 for create project\n")
    option=int(option)
    if option==1:
        listProjects()
    elif option==2:
        pass
    elif option==3:
        projectTitle=getStrData("enter project title to be deleted")
        projectDel(projectTitle)
    else:
        createProject()
    
    
def login():
    print("==========hello from login=========")
    email=emailValidation("enter your email")
    password=getPasswordData("enter your password")
    goToMenu=userIsExist({"email":email,"password":password})
    if goToMenu:
        global login_user
        login_user=email
        projectMenu()
    
    
    



def register():
    f_name=getStrData("enter your first name")
    l_name=getStrData("enter your last name")
    email=emailValidation("enter your email")
    password=getPasswordData("enter your password")
    confirmPasswoed=getPasswordData("confirm password")
    while confirmPasswoed!=password:
        print("unmatched password\n")
        password=getPasswordData("enter your password")
        confirmPasswoed=getPasswordData("confirm password")
    phone=phoneValidation("enter your phone number")
    user={"f_name":f_name,"l_name":l_name,"email":email,"password":password,"phone_number":phone}
    pushToFile(user)
    login()
    
        
    
    

def start_point():
        option=input("enter\n1 for login\n2 for register\n")
        while not option.isnumeric() or int(option) not in (1,2):
            print("invalid selection")
            option=input("1 for login\n2 for register\n")
        option=int(option)
        if option==1:
            login()
        else:
            register()
        

start_point()   
 
        
