from flask import Flask, escape, request, render_template
import delta_apk as resolver
import schedule
from datetime import datetime
import time

global last_updated1
global beers1

def update_list():
    last_updated1 = datetime.now()
    beers1 = resolver.get_beer_list()
    print("Updated list")

schedule.every().minute.do(update_list)
update_list()

app = Flask(__name__)

@app.route('/')
def apk():
    return render_template('list.html', beers=resolver.get_beer_list(), last_updated="")

if __name__ == '__main__':
    app.run()
