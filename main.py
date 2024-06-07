from flask import Flask, request, jsonify
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
import requests
from bs4 import BeautifulSoup

api_id = '28679577'
api_hash = 'fa71b2fcf8c3f5f98f172be3783bdc87'
phone_number = '+79506078464'
client = TelegramClient('session', api_id, api_hash)
client.start()

app = Flask(__name__)

@app.route('/login')
def login():
    qr_code = client.send_code_request(phone_number)
    return jsonify({'qr_code': qr_code})

@app.route('/get_messages')
def get_messages():
    messages = []
    for dialog in client.iter_dialogs():
        messages.append({'chat_id': dialog.entity.id, 'messages': client.get_messages(dialog.entity)})
    return jsonify(messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    chat_id = request.json['chat_id']
    message = request.json['message']
    input_peer = InputPeerUser(chat_id, 0)
    client.send_message(input_peer, message)
    return jsonify({'status': 'success'})

@app.route('/wild/<item>')
def wild_search(item):
    city = 'Москва'
    url = f'https://www.wildberries.ru/catalog/0/search.aspx?search={item}&city={city}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', class_='dtList i-dtList j-card-item')
    result = []
    for product in products[:10]:
        title = product.find('span', class_='goods-name').text
        link = product.find('a')['href']
        result.append({'title': title, 'link': link})
    return jsonify(result)

if __name__ == '__main__':
    app.run()

