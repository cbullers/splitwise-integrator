from .provider import Provider
import requests
import json

class CityProvider(Provider):

  def __init__(self, config):
    super().__init__(config)

    self.URLS = {
      "login": "https://billpay.olatheks.org/API/AdvancedUtility/LinkAPI/security/login",
      "data": f"https://billpay.olatheks.org/API/AdvancedUtility/BillingSummary/summary/data?custno={self.config['CUSTNO']}&acctno={self.config['ACCTNO']}"
    }

  def get_bill_amount(self):
      session = requests.Session()
      payload = {'username': self.config["USER"], 'password': self.config["PASS"], 'defaultAccount': ''}
      headers = {
          'Content-Type': 'application/x-www-form-urlencoded'
      }
      session.post(self.URLS["login"], headers=headers, data=payload)

      data = session.get(self.URLS["data"])
      data = json.loads(json.loads(data.text))

      return float(data["totalBalanceString"].replace("$",""))

  def get_current_cost(self):
    return self.get_bill_amount()
  
  def get_description(self):
    return "City" + super().get_description()