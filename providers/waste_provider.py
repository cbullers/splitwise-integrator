from .provider import Provider
import requests
from bs4 import BeautifulSoup, Tag

class WasteProvider(Provider):

  URLS = {
    "login": "https://jcwcss.jcw.org/cssgen3/public/login"
  }

  def get_csrf_token(self, session):
      r = session.get(self.URLS["login"])
      soup = BeautifulSoup(r.text, 'html.parser')
      csrf_token = soup.find('input', {'name': '_csrf'}).get('value')
      return csrf_token

  def get_current_balance(self, html_text):
      soup = BeautifulSoup(html_text, 'html.parser')

      def contains_current_balance(text):
          return 'Current Balance' in text if text else False

      balance_label = soup.find('span', string=contains_current_balance)
      balance_value = balance_label.find_next_sibling('span')
      return float(balance_value.text.replace("$",""))

  def get_bill_amount(self):
      session = requests.Session()
      token = self.get_csrf_token(session)
      payload = {'_csrf': token, 'username': self.config["USER"], 'password': self.config["PASS"]}
      headers = {
          'Content-Type': 'application/x-www-form-urlencoded'
      }
      response = session.post(self.URLS["login"], headers=headers, data=payload)

      return self.get_current_balance(response.text)

  def get_current_cost(self):
    return self.get_bill_amount()
  
  def get_description(self):
    return "Waste" + super().get_description()