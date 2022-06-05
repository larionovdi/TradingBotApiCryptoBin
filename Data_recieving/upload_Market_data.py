import pandas as pd
import websocket, json

import sqlalchemy
engine = sqlalchemy.create_engine('postgresql://postgres:Larry@localhost:5432')
candle = []

ddata_frame = pd.DataFrame()
SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"

def data_append_toSQL(df):

    global ddata_frame
    ddata_frame = ddata_frame.append(df)
    df.to_sql('market_data', engine, if_exists='append', index=False)
     


    return ddata_frame

def createframe(candle):
    df = pd.DataFrame([candle])
    
    df = df.loc[:,['s','t','c']]
    df.columns = ['symbol','Time','Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ns')
    data_append_toSQL(df)
    return(df)


def on_open(ws):
    print('open connection')
def on_close(ws):
    print('closed connection')
def on_message(ws, message):
    global candle
    #print('Received message')
    json_message = json.loads(message)
    candle = json_message['k']
    close = candle['c']
    print(close)
    is_candle_closed = candle['x']
    if is_candle_closed == True:
        print('closes')
        print('candle closed at {}'.format(close)) 
    
    createframe(candle)
    

    

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)

ws.run_forever()



