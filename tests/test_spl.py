import unittest
from splunksdk.utils.login import SplunkLogin
from splunksdk.splunk import SplunkApi

env = {
    # Splunk Enterprise host (default: localhost)
    "host": "localhost",
    # Splunk Enterprise admin port (default: 8089)
    "port": 8089,
    # Splunk Enterprise username
    "username": "admin",
    # Splunk Enterprise password
    "password": "changed!",
    # Access scheme (default: https)
    "scheme":"https",
    # Your version of Splunk Enterprise
    #"version": 8.0,
    "sharing": "system",
    "app": "search",
    "owner":"nobody",
    "verify": False,
}
    

    # Bearer token for authentication
    #bearerToken=<Bearer-token>
    # Session key for authentication
    #sessionKey=<Session-Key>


class SplunkTestCase(unittest.TestCase):

    def test_make_request(self):
        # Create a Splunk client
        client = SplunkApi(**SplunkLogin.create_from_dict(env).to_dict())

        # Make a request
        response = client.make_request('search', 'index=main sourcetype=syslog')

        # Assert that the response was successful
        self.assertEqual(response.status_code, 200)
