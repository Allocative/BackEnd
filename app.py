from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def HomePage():
   return "Allocative HomePage"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)