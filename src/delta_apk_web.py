from flask import Flask, escape, request, render_template
from apscheduler.schedulers.background import BackgroundScheduler

import delta_apk as resolver
from datetime import datetime
import time

def get_datetime():
    return str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

last_updated = ""
last_updated_time = get_datetime()
beers = resolver.get_beer_list()

def update_list():
    global beers
    global last_updated
    global last_updated_time
    try:
        beers = resolver.get_beer_list()
        last_updated_time = get_datetime()
        last_updated = "Senast uppdaterad: " + last_updated_time
        print("Updated list ", last_updated_time)
    except: 
        print("Failed to get beer list")
        last_updated = "Något gick fel vid senaste uppdatering vilket är mindre bra, använder cachad version från " + last_updated_time


app = Flask(__name__)
update_list()
sched = BackgroundScheduler(daemon=True)
sched.add_job(update_list, 'interval', hours=1)
sched.start()

@app.route('/')
def apk():
    global beers
    global last_updated
    return render_template('list.html', beers=beers, last_updated=last_updated)

if __name__ == '__main__':
    app.run()
