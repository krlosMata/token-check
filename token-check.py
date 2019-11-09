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

## Load token configuration
token = config["bitfinex"]["token"]
tokenToSell = config["bitfinex"]["amount"]

def getTotalSell(_pair):
  pair = token + _pair
  tokenBidsBtc = cliBitfinex.orderbook(symbol = pair)["bids"]
  sell = []
  totalAmount = 0
  flagFilled = False
  for bid in tokenBidsBtc: 
    amountBid = float(bid["amount"])
    priceBid = float(bid["price"])
    if ((totalAmount + amountBid) > tokenToSell):
      fillBid = tokenToSell - totalAmount
      sell.append({"amount": fillBid, "price": priceBid})
      flagFilled = True
      break
    else:
      totalAmount += amountBid
      sell.append({"amount": amountBid, "price": priceBid})
  return sell, flagFilled

def getAveragePrice(operations):
  totalSell = 0
  totalToken = 0
  for operation in operations:
    totalSell += operation["amount"] * operation["price"]
    totalToken += operation["amount"]
  return (totalSell / totalToken), totalToken

while True:
  try:
    info = "<--------------------->\n"
    info += "<---------INIT-------->\n"
    info += "<--------------------->\n\n"
    timestamp = time.strftime("%d-%m-%Y__%H;%M;%S")
    info += "TIME: {}\n".format(time.strftime("%d/%m/%Y - %H:%M:%S"))

    priceBtcUsd = float(cliBitfinex.ticker(symbol = "btcusd")["last_price"])
    priceEthUsd = priceBtcUsd * float(cliBitfinex.ticker(symbol = "ethbtc")["last_price"])
    priceUsd = 1

    tokenVolBtc = getVolume(token + "btc") * priceBtcUsd
    tokenVolEth = getVolume(token + "eth") * priceEthUsd
    tokenVolUsdt = getVolume(token + "usd") * priceUsd

    info += "<---------General--------->\n"
    info += "total to sell: " + str(round(tokenToSell, 1)) + " " + token + " \n" 
    info += "volume Btc: " + str(round(tokenVolBtc, 1)) + " Usd\n"
    info += "volume Eth: " + str(round(tokenVolEth, 1)) + " Usd\n"
    info += "volume Usdt: " + str(round(tokenVolUsdt, 1)) + " Usd\n\n"

    info += "<---------BTC--------->\n"
    sellBtc, flagBtc = getTotalSell("btc")
    avPriceBtc, totalToken = getAveragePrice(sellBtc)
    info += "amount filled: " + str(round(totalToken, 2)) + " " + token + " \n"
    info += "average price: " + str(round(avPriceBtc*priceBtcUsd, 5)) + " Usd\n"
    finalAmount = round(totalToken * avPriceBtc * priceBtcUsd, 2)
    info += str(tokenToSell) + " Nec are equivalent to " + str(finalAmount) + " Usd" + "\n\n" 

    info += "<---------ETH--------->\n"
    sellEth, flagEth = getTotalSell("eth")
    avPriceEth, totalToken = getAveragePrice(sellEth)
    info += "amount filled: " + str(round(totalToken, 2)) + " " + token + " \n"
    info += "average price: " + str(round(avPriceEth*priceEthUsd, 5)) + " Usd\n"
    finalAmount = round(totalToken * avPriceEth * priceEthUsd, 2)
    info += str(tokenToSell) + " Nec are equivalent to " + str(finalAmount) + " Usd"  + "\n\n"

    info += "<---------USDT--------->\n"
    sellUsd, flagUsd = getTotalSell("usd")
    avPriceUsd, totalToken = getAveragePrice(sellUsd)
    info += "amount filled: " + str(round(totalToken, 2)) + " " + token + " \n"
    info += "average price: " + str(round(avPriceUsd*priceUsd, 5)) + " Usd\n"
    finalAmount = round(totalToken * avPriceUsd * priceUsd, 2)
    info += str(tokenToSell) + " Nec are equivalent to " + str(finalAmount) + " Usd"  + "\n\n"

    print(info)

    botTel.sendMessage(info)
  except Exception as e: 
    line = sys.exc_info()[-1].tb_lineno
    print('Exception in line: {}\n {}'.format(line,e), flush = True)
  time.sleep(TIMEOUT)



