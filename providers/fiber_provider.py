from .provider import Provider

class FiberProvider(Provider):

  def get_current_cost(self):
    return 100
  
  def get_description(self):
    return "Fiber" + super().get_description()