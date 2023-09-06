from .provider import Provider
import requests
from bs4 import BeautifulSoup, Tag

class GasProvider(Provider):

  URLS = {
      "login": "https://www.atmosenergy.com/accountcenter/logon/login.html",
      "authenticate": "https://www.atmosenergy.com/accountcenter/logon/authenticate.html"
  }

  def get_csrf_token(self,session):
      r = session.get(self.URLS["login"])
      soup = BeautifulSoup(r.text, 'html.parser')
      csrf_token = soup.find('input', {'name': 'formId'}).get('value')
      return csrf_token

  def get_current_balance(self,html_text):
      soup = BeautifulSoup(html_text, 'html.parser')

      balance = soup.find_all('div', class_="grpAmountDue")
      return float(balance[0].text.replace("$",""))

  def get_bill_amount(self):
      session = requests.Session()
      token = self.get_csrf_token(session)
      payload = {'formId': token, 'username': self.config["USER"], 'password': self.config["PASS"], 'button.Login': 'submit'}
      headers = {
          'Content-Type': 'application/x-www-form-urlencoded'
      }
      response = session.post(self.URLS["authenticate"], headers=headers, data=payload)

      return self.get_current_balance(response.text)

  def get_current_cost(self):
    return self.get_bill_amount()
  
  def get_description(self):
    return "Gas" + super().get_description()