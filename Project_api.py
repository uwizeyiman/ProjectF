#import re
from turtle import clear
import mysql.connector as mysql
from flask import *
App = Flask(__name__)
db = mysql.connect(
    host="localhost",
    user='root',
    passwd="Kayitare",
    database="FProject_DB"
)
cursor = db.cursor()

global AlcoholData
global SugarData
global AceticData
global MethaneData


@App.route("/insert/data", methods=['GET'])
def home():
    global Alcohol
    global Sugar
    global Acetic
    global Methane

    if 'alcohol' in request.args and 'sugar' in request.args and 'acetic' in request.args and 'methane' in request.args:
        Alcohol = float(request.args.get('alcohol'))
        Sugar = float(request.args.get('sugar'))
        Acetic = float(request.args.get('acetic'))
        Methane = float(request.args.get('methane'))
        querry = "INSERT INTO SENSORS_READINGS(ALCOHOL,TOTALSUGAR,ACETICACID,METHANE) VALUES('%s','%s','%s','%s')"
        values = (Alcohol, Sugar, Acetic, Methane)
        cursor.execute(querry, values)
        db.commit()
        return "Data are inserted into Mysql Database Successfully"


@App.route("/sensors/dashboard")
def display():
    import pickle
    with open("Beer_model.sav", "rb") as f:
        model = pickle.load(f)
    quality = model.predict([[Alcohol, Sugar, Acetic, Methane, 50]])
    query = cursor.execute(
        "SELECT alcohol,totalsugar,aceticacid,methanol, AddedAt FROM SENSORS_READINGS WHERE AddedAt >= DATE_SUB(NOW(), INTERVAL 1 HOUR) ORDER BY id ASC")
    queryData = cursor.fetchall()
    query1Data = ""
    query2Data = ""
    query3Data = ""
    query4Data = ""
    addedAtData = ""

    for row in queryData:
        query1Data += str(row[0]) + ","
        query2Data += str(row[1]) + ","
        query3Data += str(row[2]) + ","
        query4Data += str(row[3]) + ","
        addedAtData += str(row[4]) + ","

    cursor.close
    db.close

    return render_template('FProject_display.html', alcohol=Alcohol, sugar=Sugar, acetic=Acetic, methane=Methane, pred=quality, AlcoholData=query1Data, SugarData=query2Data, AceticData=query3Data, MethaneData=query4Data, AddedAtData=addedAtData)


if __name__ == "__main__":
    App.run(debug=True, host='0.0.0.0')
