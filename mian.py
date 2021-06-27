import requests, time, websocket, json, xlsxwriter, _thread
from types import SimpleNamespace


def save_file(data, log):
    workbook = xlsxwriter.Workbook('data.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    for i in data:
        worksheet.write(row, 0, i[4])
        worksheet.write(row, 1, i[6])
        row = row + 1
    workbook.close()
    print(log)


time = int(time.time() * 1000) - 1000 * 60 * 60 * 24
url = 'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&startTime=%d&limit=1000' % time
response = requests.get(url)
time = response.json()[999][6]
data = response.json()
url = 'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&startTime=%d&limit=1000' % time
response = requests.get(url)
data = data + response.json()
_thread.start_new_thread(save_file, (data, "save"))


def on_message(ws, message):
    x = json.loads(message, object_hook=lambda d: SimpleNamespace(**d))

    if x.k.x:
        print(True)
        candle = [[0, 0, 0, 0, x.k.c, 0, x.k.T]]
        ws.data = ws.data + candle
        _thread.start_new_thread(save_file, (ws.data, "save"))


def on_close(ws):
    print('message')


socketUrl = 'wss://stream.binance.com:9443/ws/btcusdt@kline_1m'
ws = websocket.WebSocketApp(socketUrl, on_message=on_message, on_close=on_close)
ws.data = data
ws.run_forever()
