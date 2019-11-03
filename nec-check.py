import time, sys
from custom import general, bitfinexpy, telegram
from pathlib import Path

## Global variablesç
TIMEOUT = 2 * 60 * 60

## Path configuration file
configPath = Path.cwd().joinpath("config.json")

## Load configuration file
config = general.readJson(configPath)

## Load telegram
botTel = telegram.Ctelegram(config["telegram"]["tokenId"], config["telegram"]["chatId"])

## Load client bitfinex
cliBitfinex = bitfinexpy.API(environment = "live", key = config["bitfinex"]["key"], secret_key = config["bitfinex"]["secret"])

## Helpers Api bitfinexint
def getVolume(pair):
  res = cliBitfinex.ticker(symbol = pair)
  vol = float(res["volume"])
  lastPrice = float(res["last_price"])
  return lastPrice * vol

necToSell = config["bitfinex"]["amount"]

def getTotalSell(_pair):
  pair = "nec" + _pair
  necBidsBtc = cliBitfinex.orderbook(symbol = pair)["bids"]
  sell = []
  totalAmount = 0
  flagFilled = False
  for bid in necBidsBtc: 
    amountBid = float(bid["amount"])
    priceBid = float(bid["price"])
    if ((totalAmount + amountBid) > necToSell):
      fillBid = necToSell - totalAmount
      sell.append({"amount": fillBid, "price": priceBid})
      flagFilled = True
      break
    else:
      totalAmount += amountBid
      sell.append({"amount": amountBid, "price": priceBid})
  return sell, flagFilled

def getAveragePrice(operations):
  totalSell = 0
  totalNec = 0
  for operation in operations:
    totalSell += operation["amount"] * operation["price"]
    totalNec += operation["amount"]
  return (totalSell / totalNec), totalNec

while True:
  try:
    info = "<--------------------->\n"
    info += "<---------INIT-------->\n"
    info += "<--------------------->\n\n"
    timestamp = time.strftime("%d-%m-%Y__%H;%M;%S")
    info += "TIME: {}\n".format(time.strftime("%d/%m/%Y - %H:%M:%S"))

    priceBtcUsd = float(cliBitfinex.ticker(symbol = "btcusd")["last_price"])
    priceEthUsd = priceBtcUsd * float(cliBitfinex.ticker(symbol = "ethbtc")["last_price"])
    necVolBtc = getVolume("necbtc") * priceBtcUsd
    necVolEth = getVolume("neceth") * priceEthUsd

    info += "<---------General--------->\n"
    info += "total to sell: " + str(round(necToSell, 1)) + " Nec\n" 
    info += "volume Btc: " + str(round(necVolBtc, 1)) + " Usd\n"
    info += "volume Eth: " + str(round(necVolEth, 1)) + " Usd\n\n"

    sellBtc, flagBtc = getTotalSell("btc")
    avPriceBtc, totalNec = getAveragePrice(sellBtc)

    info += "<---------BTC--------->\n"
    info += "amount filled: " + str(round(totalNec, 2)) + " Nec\n"
    info += "average price: " + str(avPriceBtc) + " Btc\n"
    finalAmount = round(totalNec * avPriceBtc * priceBtcUsd, 2)
    info += str(necToSell) + " Nec are equivalent to " + str(finalAmount) + " Usd" + "\n\n" 

    info += "<---------ETH--------->\n"
    sellEth, flagEth = getTotalSell("eth")
    avPriceEth, totalNec = getAveragePrice(sellEth)
    info += "amount filled: " + str(round(totalNec, 2)) + " Nec\n"
    info += "average price: " + str(avPriceBtc) + " Eth\n"
    finalAmount = round(totalNec * avPriceEth * priceEthUsd, 2)
    info += str(necToSell) + " Nec are equivalent to " + str(finalAmount) + " Usd"  + "\n\n"

    botTel.sendMessage(info)
  except Exception as e: 
    line = sys.exc_info()[-1].tb_lineno
    print('Exception in line: {}\n {}'.format(line,e), flush = True)
  time.sleep(TIMEOUT)



