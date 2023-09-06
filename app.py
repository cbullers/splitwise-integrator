from dotenv import load_dotenv
from providers import *
from splitwise import Splitwise, Expense, Category
from splitwise.user import ExpenseUser
import os


provider_configs = {
    'ELECTRICITY': {
        'category': 5,
    },
    'GAS': {
        'category': 6,
    },
    'CITY': {
        'category': 7,
    },
    'WASTE': {
        'category': 37,
    },
    'FIBER': {
        'category': 8,
    }
}


def setup_providers():
    global provider_configs
    providers = []

    # Populate config dictionaries from env vars
    for key, value in os.environ.items():
        if key.startswith("PROVIDER_"):
            _, provider_type, config_key = key.split('_', 2)
            if provider_type in provider_configs:
                provider_configs[provider_type][config_key] = value

    # Initialize providers with their respective config dictionaries
    if provider_configs['ELECTRICITY']:
        providers.append({"key": "ELECTRICITY", "prov": ElectricityProvider(
            provider_configs['ELECTRICITY'])})
    if provider_configs['GAS']:
        providers.append(
            {"key": "GAS", "prov": GasProvider(provider_configs['GAS'])})
    if provider_configs['CITY']:
        providers.append(
            {"key": "CITY", "prov": CityProvider(provider_configs['CITY'])})
    if provider_configs['WASTE']:
        providers.append(
            {"key": "WASTE", "prov": WasteProvider(provider_configs['WASTE'])})
    if provider_configs['FIBER']:
        providers.append(
            {"key": "FIBER", "prov": FiberProvider(provider_configs['FIBER'])})

    return providers


if __name__ == "__main__":
    load_dotenv()
    providers = setup_providers()

    api = Splitwise(os.getenv("SPLITWISE_CONSUMER_KEY"),
                    os.getenv("SPLITWISE_CONSUMER_SECRET"),
                    api_key=os.getenv("SPLITWISE_API_TOKEN"))

    # Find the group to publish expenses to
    pub_group = os.getenv("SPLITWISE_GROUP_NAME")
    group = [g for g in api.getGroups() if g.name == pub_group][0]

    # Get existing expenses in group
    expenses = api.getExpenses(group_id=group.id)
    expenses = [e for e in expenses if e.deleted_at is None]

    # Loop providers and post expenses
    for provider in providers:
        prov = provider["prov"]
        conf = provider_configs[provider["key"]]

        # If expense already exists, skip

        if any(e.description == prov.get_description() for e in expenses):
            print("Skipping existing expense: " + prov.get_description())
            continue

        # If no data, skip
        cost = prov.get_current_cost()
        if cost <= 0:
            print("Skipping expense with cost <= 0: " + prov.get_description())
            continue

        category = Category()
        category.setId(conf["category"])

        # Create expense
        expense = Expense()
        expense.setCost(cost)
        expense.setDescription(prov.get_description())
        expense.setCategory(category)
        expense.setGroupId(group.id)
        ourself = api.getCurrentUser()
        expense_user = ExpenseUser()
        expense_user.setId(ourself.getId())
        expense_user.setPaidShare(cost)
        expense_user.setOwedShare(cost)
        expense.setUsers([expense_user])

        e, errors = api.createExpense(expense)
        if e:
            print(e.getId())
        if errors:
            print(errors.getErrors())
