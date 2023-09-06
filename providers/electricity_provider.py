from .provider import Provider
from .evergy.evergy import Evergy

class ElectricityProvider(Provider):

  def get_current_cost(self):
    ev = Evergy(self.config["USER"], self.config["PASS"])
    return ev.get_bill_amount()
  
  def get_description(self):
    return "Electricity" + super().get_description()