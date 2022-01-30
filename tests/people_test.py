from json import dumps
from uuid import uuid4
import requests
from assertpy.assertpy import assert_that, soft_assertions
from config import BASE_URI

'''
An integral part of any Test Automation Framework is the assertion library that you choose. 
A test that doesn't assert anything is of very less value.
When it comes to choose an assertion library in Python, there are many options we can choose either something 
out of your test like Unit Tests, and bunch of other modules. 
We'll use Assertpy because it has really nice syntax and gives you many of the assert functions out of the box.
It's easy to use. 
AssertPy is itself inspired from AssertJ which itself a very popular library in Java language. 
Read more in Readme file : https://github.com/assertpy/assertpy
'''


def test_read_all_has_kent():
    # We use requests.get() with url to make a get request
    response = requests.get(BASE_URI)
    # Added the soft_assertions() - we use this when we want our Tests to run successfully (means failing one/any test
    # won't stop the Test script's execution). It will Collect all the failed tests, consolidate all of them with the
    # errors and return all the failed test failures in last with the failure messages.
    with soft_assertions():
        # response from requests has many useful properties.
        # we can assert on the response status code
        assert_that(response.status_code).is_equal_to(requests.codes.ok)
        # We can convert the JSON to --> Python Dictionary as response by using .json() method
        response_content = response.json()
        # Use assertpy's fluent assertions to extract all fnames and then see the result is non-empty and has
        # 'Kent' user in it.
        assert_that(response_content).extracting('fname').is_not_empty().contains('Kent')


def test_new_person_can_be_added():
    unique_last_name = create_new_person()
    # After user is created, we read all the users and then use filter expression to find if the
    # created user is present in the response list
    peoples = requests.get(BASE_URI).json()
    is_new_user_created = search_created_user_in(peoples, unique_last_name)
    assert_that(is_new_user_created).is_not_empty()


def test_created_person_can_be_deleted():
    persons_last_name = create_new_person()
    peoples = requests.get(BASE_URI).json()
    newly_created_user = search_created_user_in(peoples, persons_last_name)[0]
    delete_url = f'{BASE_URI}/{newly_created_user["person_id"]}'
    response = requests.delete(delete_url)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)


def create_new_person():
    # Ensure a user with a unique last name is created everytime the test runs
    # Note: json.dumps() is used to convert python dict to json string
    unique_last_name = f'User {str(uuid4())}'
    payload = dumps({
        'fname': 'New',
        'lname': unique_last_name
    })
    # Setting default headers to show that the client accepts json and will send the json in the headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    # We use requests.post() method with keyword params to make the request more readable
    response = requests.post(url=BASE_URI, data=payload, headers=headers)
    assert_that(response.status_code, description='Person not created').is_equal_to(requests.codes.no_content)
    return unique_last_name


def search_created_user_in(peoples, last_name):
    return [person for person in peoples if person['lname'] == last_name]
