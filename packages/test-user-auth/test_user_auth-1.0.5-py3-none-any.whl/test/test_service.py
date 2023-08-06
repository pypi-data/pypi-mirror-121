
import os
from IdentityService.service import IdentityService
import pytest
import pandas as pd 

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
path_=os.path.join(BASE_DIR, 'test.json')

try_ = IdentityService(path_=path_)


def test_register():
    with open(path_, 'w'):
        assert os.path.isfile(path_), 'Checking path.'
        assert os.stat(path_).st_size == 0, 'Created an empty file.'
    assert try_.register('TESTUSER', 'TESTPASSWORD')==True, 'User data is written to .json file.'
    assert os.stat(path_).st_size != 0, 'User data is written to .json file.'
    assert try_.register('testuser', 'TESTPASSWORD')==False, 'Registered user.'
    assert try_.register('testuser', '11')==False, 'Short password'
    assert try_.register('ter', '11')==False, 'Short username & password'
    assert try_.register('testuser', 'DIFFERENT__TESTPASSWORD')==True, 'Added user similar name'
  

def test_authenticate():
    with open(path_, 'w'):
        assert try_.authenticate('Test','EMPTY123') == False
    assert try_.register('TESTUSER1', 'TESTPASSWORD1')==True
    assert try_.authenticate('TESTUSER1', 'TESTPASSWORD1')==False, 'Already registered user.'
    assert try_.authenticate('testuser1', 'TESTPASSWORD1')==True, 'Checking casing.'
    assert try_.authenticate('tesTuser1', 'DIFFERENT__TESTPASSWORD1')==False, 'Checking casing.'
    assert try_.authenticate('TESTuseR1', 'DIFFERENT__TESTPASSWORD2')==False, 'Already registered user.'