import get_mansion
from selenium import webdriver
from flask import Flask, render_template, request, make_response, redirect, url_for
from datetime import datetime
import pathlib
import sqlite3


XLSX_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

# flask
app = Flask(__name__, static_folder='static')


#「/」へアクセスがあった場合
@app.route("/")
def index():
    # p = pathlib.Path('../mansionProject/chromedriver')
    # print(p.cwd())
    # driver = webdriver.Chrome(p)
    # driver.get("https://door.ac/")
    contents = get_mansion.get_all()

    # conn = sqlite3.connect('teikyou_hantei.db')
    # cur = conn.cursor()
    # cur.execute('SELECT id FROM teikyou_hantei')
    # res = cur.fetchall()
    # db_id = len(res)

    return render_template("index.html", contents=contents)

@app.route("/howto")
def howto():
    return render_template("howto.html")

@app.route("/result", methods=["post"])
def post():
    try:
        load_url = request.form["url"]
        contents = get_mansion.get_mansion(load_url)
        return render_template("result.html", contents=contents)
    except:
        e = get_mansion.get_mansion(load_url).e
        return render_template("result_error.html", e=e)


@app.route('/delete/<pk>', methods=['post'])
def delete(pk):
    """ 結果削除処理 """
    conn = sqlite3.connect('teikyou_hantei.db')
    get_mansion.delete(conn, pk)
    return redirect(url_for('index'))


# @app.route('/view/<pk>', methods=['POST'])
# def delete(pk):
#     """ 結果削除処理 """
#     conn = sqlite3.connect('teikyou_hantei.db')
#     get_mansion.delete(conn, pk)
#     return render_template("index.html")

@app.route('/report/<string:report_id>', methods=['GET'])
def report3(report_id):

    response = make_response()
    response.data = open("result.xlsx", "rb").read()

    downloadFileName = report_id
    response.headers['Content-Disposition'] = 'attachment; filename=' + downloadFileName

    response.mimetype = XLSX_MIMETYPE
    return response

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    app.run(debug=True)