Flask Secrets Login with WTForms


Flask と Flask-WTF を使って作成したシンプルなログインアプリです。
セキュアなログインロジック、フォームのバリデーション、
そして入力内容に応じたページ遷移を実装しています。

A simple login app built with Flask and Flask-WTF, 
showcasing secure login logic, form validation, 
and conditional page rendering based on credentials.


📌概要 / Overview

このプロジェクトでは、以下の内容を学ぶことができます / This project demonstrates how to:
- Flask-WTFとWTFormsを使ったフォームの構築 / Build forms using Flask-WTF and WTForms
- メール形式やパスワードの長さなどのバリデーション追加 / Add validations like email format and password length
- CSRF対策の実装（悪意ある第三者による不正なリクエストを防ぐため） / Use CSRF protection
- フォームの入力内容によって表示するページを切り替えるルーティング / Create routes that return different pages based on form input


📌使用技術 / Technologies Used

- Python 3  
- Flask  
- Flask-WTF  
- WTForms  
- Jinja2 (HTML templates)
