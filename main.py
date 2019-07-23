from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

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