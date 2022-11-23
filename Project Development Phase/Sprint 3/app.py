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


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    msg=''
    if request.method == 'POST':
        age=request.form['age']
        R_value = request.form['R_button']
        userid= session['USERNAME']
        insert_sql="update DONORS set AGE=?,STATUS=? where USERNAME=?"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,age)
        ibm_db.bind_param(prep_stmt,2,R_value)
        ibm_db.bind_param(prep_stmt,3,userid)
        
        if R_value == "donor":
            if age >= '17' and age <= '60':
                ibm_db.execute(prep_stmt)
                return render_template('Request.html')
                
            else:
                msg='Your not eligible for plasma donoation!'
                return render_template('dashboard.html',msg=msg,donor_count=donor_count,request_count=request_count)
        ibm_db.execute(prep_stmt)
        return render_template('Request.html')

