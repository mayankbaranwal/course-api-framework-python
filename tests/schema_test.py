import json
import requests
from assertpy import assert_that, soft_assertions
from cerberus import Validator
from config import BASE_URI

''' 
Chapter 6 - API Response Schema Validation
https://docs.python-cerberus.org/en/stable/
So, the main CRUDs of the Cerberus is actually the Schema and it's a disctionary like structure as we can see below,
that they define. Cerberus defines its own sort of mini language to define the schemas as well as their types.

'''
schema = {
    "fname": {'type': 'string'},
    "lname": {'type': 'string'},
    "person_id": {'type': 'number'},
    "timestamp": {'type': 'string'}
}


def test_read_one_operation_has_expected_schema():
    response = requests.get(f'{BASE_URI}/1')
    person = json.loads(response.text)
    '''
    Below is the main logic, how Cerberus works. We create an object of the Validator class and passing the 'schema'
    dictionary that we've already created. Notice, the second argument 'require_all=True' , this is a global flag that 
    we can set for this particular 'schema' specifying that all the keys in this response are required. So, if for 
    some reason our API tomorrow skips any field we will get an error. 
    '''
    validator = Validator(schema, require_all=True)
    is_valid = validator.validate(person)

    assert_that(is_valid, description=validator.errors).is_true()


def test_read_all_operation_has_expected_schema():
    response = requests.get(BASE_URI)
    persons = json.loads(response.text)

    validator = Validator(schema, require_all=True)

    with soft_assertions():
        for person in persons:
            is_valid = validator.validate(person)
            assert_that(is_valid, description=validator.errors).is_true()
