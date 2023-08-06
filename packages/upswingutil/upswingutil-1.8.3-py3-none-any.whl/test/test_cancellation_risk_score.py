import unittest
from upswingutil.ml import CancellationRiskScore
import upswingutil as ul

ul.ENCRYPTION_SECRET = "S1335HwpKYqEk9CM0I2hFX3oXa5T2oU86OXgMSW4s6U="
ul.MONGO_URI = "mongodb://AdminUpSwingGlobal:Upswing098812Admin0165r@dev.db.upswing.global:27017/?authSource=admin&readPreference=primary&appname=Agent%20Oracle%20Dev&ssl=false"
ul.G_CLOUD_PROJECT = "aura-staging-31cae"
ul.FIREBASE = "/Users/harsh/upswing/github/api-oracle/SECRET/aura-staging-31cae-firebase-adminsdk-dyolr-7c135838e9.json"
ul.LOG_LEVEL_VALUE = 'DEBUG'



class TestCancellationRiskScore(unittest.TestCase):

    def test_creating_model_for_rms(self):
        """ Train and store model for RMS """
        crf = CancellationRiskScore('11249', '11263')
        # crf = CancellationRiskScore('OHIPSB', 'SAND01')
        crf.train()

    def test_predict_from_model_rms(self):
        crf = CancellationRiskScore('11249', '11263')
        result = crf.predict('', '', '', '')
        print(result)


if __name__ == '__main__':
    unittest.main()
