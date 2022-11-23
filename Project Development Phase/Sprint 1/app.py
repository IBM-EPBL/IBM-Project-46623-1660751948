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

conn= ibm_db.connect("DATABASE=;HOSTNAME=;PORT=;SECURITY=;SSLSeverCertificate=;UID=lw;PWD=",'','')

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = ''
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    

sql ="select * from Count_Values"
stmt=ibm_db.exec_immediate(conn,sql)
ibm_db.fetch_row(stmt)

donor_count =ibm_db.result(stmt,0)
request_count = ibm_db.result(stmt,1)
userid =''



@app.route('/register',methods=['GET','POST'])
def register():
    global userid
    msg=''
    if request.method == 'POST':
        username= request.form['username']
        email=request.form['email']
        password= request.form['password']
        sql="SELECT * FROM DONORS WHERE USERNAME=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg= 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg='Invalid email'
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg='name must contain only alpha characters or numbers!'
        else:
            insert_sql="INSERT INTO DONORS(USERNAME,EMAIL,PASSWORD)VALUES(?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt, 3,password)
            ibm_db.execute(prep_stmt)

            session['USERNAME'] =username
            msg='you have successfully registered!'
    elif request.method == 'POST':
        msg= "Please fill out the form"
    print(msg)
    return render_template( 'Register_2.html', msg=msg,userid=username)

@app.route('/secondregister',methods=['GET','POST'])
def secondregister():
    global userid
    msg=''
    if request.method == 'POST':
        address= request.form['address']
        phone=request.form['phone']
        blood_type= request.form['blood_type']
        userid= session['USERNAME']

        insert_sql="update DONORS set ADDRESS=?,MOBILE_NO=?,BLOOD_TYPE=? where USERNAME=?"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,address)
        ibm_db.bind_param(prep_stmt,2,phone)
        ibm_db.bind_param(prep_stmt,3,blood_type)
        ibm_db.bind_param(prep_stmt,4,userid)
        ibm_db.execute(prep_stmt)
        msg='you have successfully registered!'
    else:
        msg= "Please fill out the form"
    print(msg)
    return render_template( 'login.html', msg=msg,donor_count=donor_count,request_count=request_count)
