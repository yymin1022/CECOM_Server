from flask import Flask, send_file, request, redirect
from firebase_admin import firestore
import firebase_admin

app = Flask(__name__)

cred = firebase_admin.credentials.Certificate("cecom-server-firebase-adminsdk-1mf58-16b08d04a2.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/', methods=["GET"])
def main():
    # Firebase의 Firestore에서 접속이 차단된 IP주소 목록을 Dictionary 형식으로 저장
    bannedIP = db.collection(u'connection_ban').document(u'IP').get().to_dict()

    # 현재 접속한 클라이언트의 IP주소를 받아와 ipAddr 변수에 저장
    ipAddr = str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    print("New Connection from " + ipAddr)

    # ipAddr이 bannedIP에 속하는 경우 파일 목록을 보여주지 않고 차단메시지를 return함
    for i in list(bannedIP.values()):
        if i == ipAddr:
            print("Result : BANNED USER")
            return "현재 접속한 사용자(IP주소 : " + ipAddr + ")는 접속이 차단된 사용자입니다."
        else:
            print("Result : OK")
            return redirect('/file_list')

# 파일 목록을 표시하는 페이지
# 파일 목록 팀에서 코딩한 내용 연결시킬 것
@app.route('/file_list')
def file_list():
    pass

# 파일 목록에서 파일 선택시 filename 변수의 값을 해당 파일의 절대경로로 지정한 후 /download_file 페이지로 연결하면 다운로드 시작
# 예시로 TODO.txt 라는 이름의 파일을 다운로드하도록 지정
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