#!/usr/bin/env python
from IdentityService.service import IdentityService
import os
# import pytest

# pytest


file_name_option = input(
    'Do you want to specify a different \
    \n from default ("data_file.json) file name? (Y/N) ')
if file_name_option.lower()=="y":
    data_file_name=input('Specify file name: ')
    data_file_name = data_file_name+'.json'
    path_=os.path.join(os.getcwd(), data_file_name)
    service = IdentityService(path_=path_)

else: service = IdentityService()



def crucial_credentials():
    #DRY
    username=input('*USERNAME: ')
    password=input('*PASSWORD: ')

    return username, password

while True:
    
    intro_choice=input('Do you want to authinticate user? (Y/N) ')
    if intro_choice.lower()=='y':
        auth=crucial_credentials()
        if service.authenticate(*auth):
            print('User is registerd.')
        else: print('User is not registered.')
    elif intro_choice.lower()!='y':
        register_choice=input('Do ou want regiser a new user? Y/N: ')
        if register_choice.lower()=='y':
            username, password = crucial_credentials()
            properties={}
            properties['age']=input('Enter your age: ')
            properties['sex']=input('Enter your sex: ')
            service.register(username, password, **properties)
        
        else: 
            pass

