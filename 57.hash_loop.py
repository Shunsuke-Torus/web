# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 20:56:58 2021
概要
    ストレッチング
    web認証システムについて学ぶ
参考文献
https://www.tohoho-web.com/python/list.html
https://techacademy.jp/magazine/18885
文字列型とバイト型
#digest = hashlib.sha256(salt + digest).hexdigest()
#can't concat str to bytes
一言
hashは限りなく不可逆
str と　bytesの違い
ファイル保存が直接可能か否か知らなかった...
ちなみにsp.randprime(pow(10,1),pow(10,2))のループ時間は0.0だが
sp.randprime(pow(10,8),pow(10,9))のループは約15分かかる。
for文が悪いのかな？
今度while文との比較をしたい。
Google Colaboratory　GPUモード　無料版

7/24
値にNoneを代入するが2回目の時に問題がでるから後で直す。
tryによって無限できるようにする
txtを読み込んで、情報を得た後で、登録できてないならば、txtに書き込めるシステムにする。

@author: shun
"""

import base64
import os
import hashlib
import sympy as sp
import time
import sys

def main():
    try:
        user_name,user_pass = log_in()
    # =============================================================================
    #     登録とログインの条件分岐についての処理を明日書く
    # =============================================================================
        db,db_salt,db_n = {},{},{}
        #db_user_pass,db_user_salt,db_user_n = {},{},{}#dict　辞書 キーと値のリスト
        
        salt = base64.b64encode(os.urandom(32))
        
        n = sp.randprime(pow(10,1),pow(10,2))
        
        #辞書型にして大量に情報を蓄積
        db_salt[user_name] = salt
        db_n[user_name] = n
        db[user_name] = get_digest(user_name,user_pass,db,db_salt,db_n)
        
        print(db_salt[user_name])
        print(db_n[user_name])
        print(db[user_name])
        
        user_name,user_pass = log_in()
        
        judge = is_login(user_name,user_pass,db,db_salt,db_n)
        if judge == True:
            print("Welcome to world")
        else:
            raise ValueError
        
    except ValueError:
        print("ユーザＩＤまたはパスワードが正しくありません。")
    

def log_in():
    user_name = input("ユーザー名 \n>>")
    user_pass = input("パスワード \n>>")
    return user_name,user_pass
        

def dictonary(user_name,user_pass,db,db_salt,db_n):
    
    db_salt.setdefault(user_name, None)#値が登録されていないならNoneを追加する。
    
    
    if db_salt[user_name] == None :
        return False,False #False
    else:
        salt = db_salt[user_name]
        n = db_n[user_name]
        return salt,n
    
def is_login(user_name,user_pass,db,db_salt,db_n):
    return get_digest(user_name,user_pass,db,db_salt,db_n) == db[user_name]

def get_digest(user_name,user_pass,db,db_salt,db_n):
    try:
        start = time.time()
        salt,n = dictonary(user_name,user_pass,db,db_salt,db_n)
        if salt == False:   
            raise ValueError
        password = bytes(user_pass, 'utf-8')
        digest = hashlib.sha256(salt + password).hexdigest()
        for i in range(0,n):
            digest = hashlib.sha256(bytes(digest, 'utf-8')).hexdigest()
        elapsed_time = time.time() - start
        print(elapsed_time)
        return digest
    
    except ValueError:
        print("ユーザＩＤまたはパスワードが正しくありません。")
        sys.exit()
        

if __name__ == "__main__":
    main()
