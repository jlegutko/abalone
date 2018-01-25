from flask import Flask

app = Flask(__name__)

from abalone import views

