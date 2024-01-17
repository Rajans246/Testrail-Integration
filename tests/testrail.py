"""TestRail API binding for Python 3.x.

(API v2, available since TestRail 3.0)

Compatible with TestRail 3.0 and later.

Learn more:

http://docs.gurock.com/testrail-api2/start
http://docs.gurock.com/testrail-api2/accessing

Copyright Gurock Software GmbH. See license.md for details.
"""

import base64
import json

import requests



class APIClient:
    def __init__(self, base_url):
        self.user = ''
        self.password = ''
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/api/v2/'

    def send_get(self, uri, filepath=None):
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for 'get_attachment/:attachment_id'.

        Returns:
            A dict containing the result of the request.
        """

        return self.__send_request('GET', uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        # print("dataaa in test rail ")
        # print(data)
        # print("data successfull posted")
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        # print("data entered ___send request")
        url = self.__url + uri
        # print(url)
        
        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {'Authorization': 'Basic ' + auth}
        # print("metho")
        # print(method)
        # print("headerrrr")
        # print(headers)
        if method == 'POST':
            # print(uri)
            if uri[:14] == 'add_attachment':    # add_attachment API method
                
                # print("data entered first method in __send")
                # print(url)
                # print("uri")
                # print(uri)
                files = {'attachment': (open(data, 'rb'))}
                # print(files)
                response = requests.post(url, headers=headers, files=files)
                # print("tesponse")
                # print(response)
                files['attachment'].close()
            else:
                
                # print("data entered second else method in __send")
                # print(url)
                headers['Content-Type'] = 'application/json'
                payload = bytes(json.dumps(data), 'utf-8')
                # print("payloooooad")
                # print(payload)
                response = requests.post(url, headers=headers, data=payload)
                # print("responsee is a")
                # print(response)
        else:
            
            # print("data entered total else method in __send")
            headers['Content-Type'] = 'application/json'
            response = requests.get(url, headers=headers)
            # print("response in testrail util")
            # print(response)

        if response.status_code > 201:
            try:
                error = response.json()
                # print(url)
            except:     # response.content not formatted as JSON
                # print(url)
                # print("url in except")
                error = str(response.content)
                
            raise APIError('TestRail API returned HTTP %s (%s)' % (response.status_code, error))
        else:
            if uri[:15] == 'get_attachment/':   # Expecting file, not JSON
                try:
                    open(data, 'wb').write(response.content)
                    return (data)
                except:
                    return ("Error saving attachment.")
            else:
                try:
                    return response.json()
                except: # Nothing to return
                    return {}



class APIError(Exception):
    pass
