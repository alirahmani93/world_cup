import json

import requests

from world_cup.settings import SEND_SMS_VERIFY

sms_verify_url = SEND_SMS_VERIFY


class SMSAdapter(object):

    def pattern(self, mode):
        return mode

    def send_sms(self, receptor, token, template):
        res = requests.post(
            url=sms_verify_url,
            data={
                'receptor': receptor,
                'token': token,
                'template': template
            }
        )
        res = json.loads(res.text)
        if res['return'] and res['return']['status']:
            data = {'status': res['return']['status']}
        else:
            data = {'status': 500}

        return data


sms_adapter = SMSAdapter()
