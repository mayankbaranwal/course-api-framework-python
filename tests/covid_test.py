import requests
from assertpy import assert_that
from lxml import etree
from config import COVID_TRACKER_HOST
from utils.print_helpers import pretty_print


def test_covid_cases_have_crossed_a_million():
    """
    Learn more about 'lxml' at : https://lxml.de/xpathxslt.html
    like : how to deal with xml response.
    If you're dealing with an XML request, a common approach to deal with that, we can store our xml into a file,
    and read it from there, and then use the same method to convert it into an elementary object and then modify as per
    our need (maybe again convert into a string). So, this library offers lots of flexibility for your use cases.
    Making a request to dummy service, running on my local host : http://127.0.0.1:3000/
    """
    response = requests.get(f'{COVID_TRACKER_HOST}/api/v1/summary/latest')
    pretty_print(response.headers)
    # getting XML text
    response_xml = response.text
    """ 
    In immediate below code line we're deserializing it into an XML Object, which we can work with. 
    this ensures that you're able to convert your string into a actual tree that you can work with.
    But, the main use case with XML is typically you want to verify a whether a certain node has a certain value.
    So, for that we're using : xml_tree.xpath('pass your xpath for the node that you're actually looking for') below 
    in next code line. 
    """
    xml_tree = etree.fromstring(bytes(response_xml, encoding='utf8'))
    """ use .xpath on xml_tree object to evaluate the expression
    this below Xpath is coming from the 'Covid Tracker' API in 'people-api' project. For more detail check Postman.
    Screenshot attached for reference.
    """
    total_cases = xml_tree.xpath("//data/summary/total_cases")[0].text
    pretty_print(total_cases)
    assert_that(int(total_cases)).is_greater_than(1000000)


def test_overall_covid_cases_match_sum_of_total_cases_by_country():
    response = requests.get(f'{COVID_TRACKER_HOST}/api/v1/summary/latest')
    pretty_print(response.headers)
    response_xml = response.text
    xml_tree = etree.fromstring(bytes(response_xml, encoding='utf8'))
    overall_cases = int(xml_tree.xpath("//data/summary/total_cases")[0].text)
    # Another way to specify XPath first and then use to evaluate on an XML tree
    search_for = etree.XPath("//data//regions//total_cases")
    cases_by_country = 0
    for region in search_for(xml_tree):
        cases_by_country += int(region.text)
    assert_that(overall_cases).is_greater_than(cases_by_country)
