import get_mansion
from flask import Flask, render_template, request, make_response, redirect, url_for
import sqlite3
import set_mappin

XLSX_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

# flask
app = Flask(__name__, static_folder='static')


#「/」へアクセスがあった場合
@app.route("/")
def index():
    conn = sqlite3.connect('teikyou_hantei.db')
    cur = conn.cursor()
    if get_mansion.table_isexist(conn, cur) == False:
        get_mansion.create_table(conn, cur)
        set_mappin.mappin_create_table()
        contents = ""
    else:
        contents = get_mansion.get_all()

    return render_template("index.html", contents=contents)

@app.route("/howto")
def howto():
    return render_template("howto.html")

@app.route("/result", methods=["post"])
def post():
    try:
        load_url = request.form["url"]
        contents = get_mansion.get_mansion(load_url)
        return render_template("result.html", contents=contents, transaction_id=contents[4])
    except:
        # e = get_mansion.get_mansion().e
        return render_template("result_error.html")


@app.route('/delete/<pk>', methods=['post'])
def delete(pk):
    """ 結果削除処理 """
    conn = sqlite3.connect('teikyou_hantei.db')
    get_mansion.delete(conn, pk)
    return redirect(url_for('index'))

@app.route('/delete_result/<pk>', methods=['post'])
def delete_result(pk):
    """ 結果削除処理 """
    conn = sqlite3.connect('teikyou_hantei.db')
    get_mansion.delete(conn, pk)
    return redirect(url_for('result'))


@app.route('/set_all_mappin', methods=['GET'])
def call_all_setpin():
    """ ピン植え処理 """
    set_mappin.set_all_mappin()
    return redirect(url_for('index'))

@app.route('/set_mappin/<transaction_id>', methods=['GET'])
def call_setpin(transaction_id):
    """ ピン植え処理 """
    transaction = transaction_id[4]
    set_mappin.set_mappin(transaction)
    return redirect(url_for('index'))



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
    app.run(debug=True, host='0.0.0.0', port='5000')