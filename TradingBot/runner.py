from oanda_api import OandaAPI

api = OandaAPI()
while True:
    command = input("Enter Comamand:")
    if command == "T":
        print("Make Trade")
        trade_id = api.place_trade("EUR_USD", 1000)
        print(trade_id)
    if command == "Q":
        break