"""TestRail API client
"""

import base64
import json
import requests


class Apiclient:
    def __init__(self, base_url):
        self.user = ''
        self.password = ''
        if not base_url.endswith('/'):
            base_url = f'{base_url}/'
        self.__url = f'{base_url}index.php?/api/v2/'  

    def send_get(self, uri, filepath=None):
        """Issue a GET request.
        """
        return self.__send_request('GET', uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request.
        """
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri

        auth = str(base64.b64encode(bytes(f'{self.user}:{self.password}', 'utf-8')), 'ascii').strip()
        headers = {'Authorization': 'Basic ' + auth}

        if method == 'POST':
            if uri[:14] == 'add_attachment':    # add_attachment API method
                files = {'attachment': (open(data, 'rb'))}
                response = requests.post(url, headers=headers, files=files)
                files['attachment'].close()
            else:
                headers['Content-Type'] = 'application/json'
                payload = bytes(json.dumps(data), 'utf-8')
                response = requests.post(url, headers=headers, data=payload)
        else:
            headers['Content-Type'] = 'application/json'
            response = requests.get(url, headers=headers)

        if response.status_code > 201:
            try:
                error = response.json()
            except:     # response.content not formatted as JSON
                error = str(response.content)
            raise Exception(f'TestRail API returned HTTP {response.status_code} ({error})')
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


