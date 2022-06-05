#BOT


import pandas as pd
import websocket, json, pprint, numpy
import configTest
from binance.client import Client
import binance.spot
from binance.enums import *
from ta import momentum


client = Client(configTest.API_KEY_Test, configTest.SECRET_KEY_Test, testnet=True)

RSI_period = 14
RSI_overbought = 70
RSI_oversold = 30


closes = []

in_position = False

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
def on_open(ws):
    print('open connection')
def on_close(ws):
    print('closed connection')
def on_message(ws, message):
    global closes
    print('Received message')
    json_message = json.loads(message)
    
    pprint.pprint(json_message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed == True:
        print('candle closed at {}'.format(close))
        closes.append(float(close))
        print('closes')
        print(closes)

#Здесь описана логика робота
        if len(closes)>14:
            closes_series = pd.Series(closes)
            print(closes_series)
            rsi_series = momentum.rsi(closes_series, window = 14)

            print(rsi_series)
            last_rsi = rsi_series.iloc[-1]
            print('Last rsi {}'.format(last_rsi)) 

            #Short
            if last_rsi > RSI_overbought:
                if in_position==False:
                    print("Overbought! Sell! Sell! Sell!")
                    # put binance sell logic here
                    order_succeeded = client.order_market_sell(
                        symbol='BTCUSDT',
                        quantity=0.0005)
                    if order_succeeded:
                        in_position = False
                else:
                    print("It is overbought, but we don't own any. Nothing to do.")

            
#long
            if last_rsi < RSI_oversold:
                if in_position:
                    print("It is oversold, but you already own it, nothing to do.")
                else:
                    print("Oversold! Buy! Buy! Buy!")
                    # put binance buy order logic here
                    order_succeeded = client.order_market_buy(
                        symbol='BTCUSDT',
                        quantity=0.0005)
                    if order_succeeded:
                        in_position = True
            

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
