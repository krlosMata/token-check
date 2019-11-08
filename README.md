# token-check

Analyze Btc, Eth and Usd markets for any token and send infornation to telegram channel.

- Gets full order book for token/btc, token/eth, token/usd
- Gets volume traded over last 24h
- Calculate average price if certain token amount is wanted to sell

* Note that all api calls are public calls

## Configuration

All configuration should be store in repository path root inside a file `config.json`

```json
{
  "telegram": {
    "tokenId": "Your token id",
    "chatId": your number chat id
  },
  "bitfinex": {
    "key": "your api public key",
    "secret": "your api secret key",
    "amount": your token amount you want to sell,
    "token": "token symbol"
  }
}
```

## Usage

Once the configuration file is set, go to repository root:

install all dependencies:
`pip install -r requirements.txt`

run software:
`python3 token-check.py`