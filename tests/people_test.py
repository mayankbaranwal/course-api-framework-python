from json import dumps
from uuid import uuid4

import requests
from assertpy.assertpy import assert_that, soft_assertions

from config import BASE_URI


def test_read_all_has_kent():
    # We use requests.get() with url to make a get request
    response = requests.get(BASE_URI)
    # Added the soft_assertions() - we use this when we want our Test to run successfully (means failing one test won't
    # stop the Test script's execution). Collect all the failures, consolidate all the errors and return all the test
    # failures in last.
    with soft_assertions():
        # response from requests has many useful properties
        # we can assert on the response status code
        assert_that(response.status_code).is_equal_to(requests.codes.ok)
        # We can get python dict as response by using .json() method
        response_content = response.json()

        # Use assertpy's fluent assertions to extract all fnames and then see the result is non empty and has
        # Kent in it.
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

    # Setting default headers to show that the client accepts json
    # And will send json in the headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # We use requests.post method with keyword params to make the request more readable
    response = requests.post(url=BASE_URI, data=payload, headers=headers)
    assert_that(response.status_code, description='Person not created').is_equal_to(requests.codes.no_content)
    return unique_last_name


def search_created_user_in(peoples, last_name):
    return [person for person in peoples if person['lname'] == last_name]
