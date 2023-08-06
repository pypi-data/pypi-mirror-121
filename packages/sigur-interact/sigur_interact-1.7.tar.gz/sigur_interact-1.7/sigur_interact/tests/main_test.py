from sigur_interact.main import SigurSDK
from sigur_interact.tests import settings_test as s
import unittest
import time


class TestSigur(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.sigur_sdk = SigurSDK(s.contr_ip, s.contr_port, 3, 1, 4, 2, test_mode=False)

    def test_get_status(self):
        while True:
            response = self.sigur_sdk.get_point_status_parsed(3)
            print(response)
            time.sleep(0.5)
