from __future__ import print_function
from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re

import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

app=Flask(__name__)

app.secret_key='a'

conn= ibm_db.connect("DATABASE=;HOSTNAME=;PORT=;SECURITY=;SSLSeverCertificate=;UID=;PWD=",'','')

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = ''
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    

sql ="select * from Count_Values"
stmt=ibm_db.exec_immediate(conn,sql)
ibm_db.fetch_row(stmt)

donor_count =ibm_db.result(stmt,0)
request_count = ibm_db.result(stmt,1)
userid =''


@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg=''

    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        sql="SELECT * FROM DONORS WHERE EMAIL=? AND PASSWORD=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id']=account['USERNAME']
            userid= account['USERNAME']
            session['USERNAME'] =account['USERNAME']
            msg = 'Logged in successfully!'

            return render_template('dashboard.html',msg=msg,donor_count=donor_count,request_count=request_count)
        else:
            msg='Incorrect username/password!'
    return render_template('login.html',msg=msg)

