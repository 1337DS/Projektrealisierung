from tkinter import W
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import yfinance as yf
from main_backend import get_recommendation as get_rec
import time
import threading
import random
# create the Flask app
app = Flask(__name__)

@app.route('/')
def query_test():
    return redirect(url_for('query'))

@app.route('/fragebogen')
def query():
    return render_template("fragebogen.html")

@app.route('/info')
def info():
    return render_template("info.html")

@app.route('/auswertung')

def form_example():
    df_complete=pd.read_pickle("./Data/df_esg_final")
    animal_var=request.args.get('animal')
    tobacco_var=request.args.get('tobacco')
    alcohol_var=request.args.get('alc')
    weapons_var=request.args.get('weapons')
    risk_var=int(request.args.get('risk1'))
    esg_var=int(request.args.get('esg'))
    social_var=int(request.args.get('social'))
    beta_schwellwert=(df_complete['beta'].max()-df_complete['beta'].min())/10*risk_var
    social_schwellwert=(df_complete['socialScore'].max()-df_complete['socialScore'].min())/10*esg_var
    esg_schwellwert=(df_complete['totalEsg'].max()-df_complete['totalEsg'].min())/10*social_var
    
    
    df_filtered=df_complete
    if tobacco_var==True:
      df_filtered=df_filtered[(df_filtered['tobacco']==False)]
    if alcohol_var==True:
      df_filtered=df_filtered[(df_filtered['alcoholic']==False)]
    if animal_var==True:
      df_filtered=df_filtered[(df_filtered['animalTesting']==False)]
    if weapons_var==True:
      df_filtered=df_filtered[(df_filtered['smallArms']==False)&(df_filtered['controversialWeapons']==False)] 
    else:
      pass


    df_filtered=df_filtered[(df_filtered['totalEsg']<esg_schwellwert)]
    df_filtered=df_filtered[(df_filtered['beta']<beta_schwellwert)]
    df_filtered=df_filtered[(df_filtered['socialScore']<social_schwellwert)]
    print('top betas')
    print(df_filtered['beta'])
    print(df_filtered.head(n=10).to_string(index=False))

# nach beta sortieren
    df_filtered=df_filtered.sort_values(by=['beta'], ascending=False)
    print(df_filtered['beta'])    

# hier sentimentanalyse
    try:
        df_rec=get_rec(df_filtered)
        # sortiere df_rec
        df_filtered=df_filtered.sort_values(by=['beta'], ascending=False)

        aktie1=df_rec['long_name'][0]
        aktie2=df_rec['long_name'][1]
        aktie3=df_rec['long_name'][2]
        preis1=df_rec['last_price'][0]
        preis2=df_rec['last_price'][1]
        preis3=df_rec['last_price'][2]
        esg1=df_rec['totalEsg'][0]
        esg2=df_rec['totalEsg'][1]
        esg3=df_rec['totalEsg'][2]
        beta1=df_rec['beta'][0]
        beta2=df_rec['beta'][1]
        beta3=df_rec['beta'][2]
        print(df_rec)
        print("Eingabe Tiere",animal_var)
        print("Eingabe Alk",alcohol_var)
    except:
        return render_template("error.html")
        
    return render_template("auswertung.html", aktie1=aktie1, aktie2=aktie2, aktie3=aktie3, preis1=preis1, preis2=preis2, preis3=preis3, esg1=esg1, esg2=esg2, esg3=esg3, beta1=beta1, beta2=beta2, beta3=beta3)


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)

