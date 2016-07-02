import json
import requests
from requests_toolbelt import MultipartEncoder

DEFAULT_API_VERSION = 2.6

class Bot(object):
    def __init__(self, access_token, api_version=DEFAULT_API_VERSION, app_secret=None):
        self.api_version = api_version
        self.access_token = access_token
        self.base_url = (
            "https://graph.facebook.com"
            "/v{0}/me/messages?access_token={1}"
        ).format(self.api_version, access_token)

        if app_secret is not None:
            appsecret_proof = generate_appsecret_proof(access_token, app_secret)
            self.base_url += '&appsecret_proof={0}'.format(appsecret_proof)

    def get_user_info(self, recipient_id):

        url = ("https://graph.facebook.com/v{0}/{1}?access_token={2}" + \
               "&fields=first_name,last_name,profile_pic,locale,timezone,gender"
              ).format(self.api_version, recipient_id, self.access_token)
        r = requests.get(url)
        return r.json()

    def send_typing(self, recipient_id):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'sender_action': 'typing_on'
        }
        return self._send_payload(payload)

    def send_text_message(self, recipient_id, message):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': message
            }
        }
        return self._send_payload(payload)

    def send_message(self, recipient_id, message):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': message
        }
        return self._send_payload(payload)

    def send_generic_message(self, recipient_id, elements):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": elements
                    }
                }
            }
        }
        return self._send_payload(payload)

    def send_button_message(self, recipient_id, text, buttons):
        payload = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": buttons
                    }
                }
            }
        }
        return self._send_payload(payload)

    def _send_payload(self, payload):
        result = requests.post(self.base_url, json=payload).json()
        return result

    def send_image(self, recipient_id, image_path):
        '''
            This sends an image to the specified recipient.
            Image must be PNG or JPEG.
            Input:
              recipient_id: recipient id to send to
              image_path: path to image to be sent
            Output:
              Response from API as <dict>
        '''
        payload = {
            'recipient': json.dumps(
                {
                    'id': recipient_id
                }
            ),
            'message': json.dumps(
                {
                    'attachment': {
                        'type': 'image',
                        'payload': {}
                    }
                }
            ),
            'filedata': (image_path, open(image_path, 'rb'))
        }
        multipart_data = MultipartEncoder(payload)
        multipart_header = {
            'Content-Type': multipart_data.content_type
        }
        return requests.post(self.base_url, data=multipart_data, headers=multipart_header).json()

    def send_image_url(self, recipient_id, image_url):
        ''' Sends an image to specified recipient using URL.
            Image must be PNG or JPEG.
            Input:
              recipient_id: recipient id to send to
              image_url: url of image to be sent
            Output:
              Response from API as <dict>
        '''
        payload = {
            'recipient': json.dumps(
                {
                    'id': recipient_id
                }
            ),
            'message': json.dumps(
                {
                    'attachment': {
                        'type': 'image',
                        'payload': {
                            'url': image_url
                        }
                    }
                }
            )
        }
        return self._send_payload(payload)
