import requests
import pandas as pd
import json
from flask import Flask, request, Response
import os

from credentials import token, chat_id

# constants
TOKEN = token

# bot info
# f'https://api.telegram.org/bot{TOKEN}/getMe'

# get updates
# f'https://api.telegram.org/bot{TOKEN}/getUpdates'

# send message
# f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text='

# Webhook
# f'https://api.telegram.org/bot{TOKEN}/setWebhook?url='

def send_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}'
    r = requests.post(url, json = {'text' : text})
    print(f'Status Code send_message {r.status_code}')

    return None

def load_dataset(store_id : int):
    # loading test dataset
    df10 = pd.read_csv('test.csv' )
    df_store_raw = pd.read_csv('store.csv')

    # merge test dataset + store
    df_test = pd.merge( df10, df_store_raw, how='left', on='Store' )

    # choose store for prediction
    df_test = df_test[df_test['Store'] == store_id]

    if not df_test.empty:
        # remove closed days
        df_test = df_test[df_test['Open'] != 0]
        df_test = df_test[~df_test['Open'].isnull()]
        df_test = df_test.drop( 'Id', axis=1 )

        # convert Dataframe to json
        data = json.dumps( df_test.to_dict( orient='records' ) )
    
    else:
        data = 'error'

    return data

def predict(data):
    # API Call
    url = 'https://rossmann-model-deploy-test.herokuapp.com/rossmann/predict'
    header = {'Content-type': 'application/json' }

    r = requests.post( url, data=data, headers=header )
    print( 'Status Code predict {}'.format( r.status_code ) )

    d1 = pd.DataFrame( r.json(), columns=r.json()[0].keys() )

    return d1

# Instantiate Flask
app = Flask (__name__)

def parse_message(message):
    chat_id = message['message']['chat']['id']
    store_id = message['message']['text']

    store_id = store_id.replace('/', '')

    try:
        store_id = int(store_id)
    except ValueError:
        store_id = 'error'

    return chat_id, store_id

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.get_json()
        chat_id, store_id = parse_message(message)

        if store_id != 'error':
            # loading data
            data = load_dataset(store_id)

            if data != 'error':
                # prediction
                d1 = predict(data)
                
                # calculation
                d2 = d1[['store', 'prediction']].groupby( 'store' ).sum().reset_index()
                
                # send message
                msg =  'Store Number {} will sell R${:,.2f} in the next 6 weeks'.format( 
                            d2['store'].values[0], 
                            d2['prediction'].values[0] )

                send_message(TOKEN, chat_id, msg)
                return Response('OK', status = 200)
            
            else:
                send_message(TOKEN, chat_id, 'Store Not Available.')
                return Response('OK', status = 200)
        else:
            send_message(TOKEN, chat_id, 'Store ID is wrong.')
            return Response('OK', status = 200)
    else:
        return '<h1> Rossmann Telegram BOT </h1>'

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host = '0.0.0.0', port = port)