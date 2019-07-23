from flask import Flask, send_file, request
from firebase_admin import firestore
import firebase_admin

app = Flask(__name__)

cred = firebase_admin.credentials.Certificate("cecom-server-firebase-adminsdk-1mf58-2dcbd52a85.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/', methods=["GET"])
def main():
    result = db.collection(u'connection_ban').document(u'IP').get().to_dict()
    print(result)
    ipAddr = str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    return ipAddr

#파일 목록에서 다운로드 함수 호출시 해당 파일의 경로 지정
filename = "TODO.txt"

@app.route('/download_file')
def download_file():
    file_name = filename
    return send_file(file_name,
                     mimetype='unknown',
                     attachment_filename='filename',
                     as_attachment=True)

if __name__ == '__main__':
    app.run()