#!flask/bin/python
from abalone import app
app.run(host='0.0.0.0', port=5019, debug=False)
#app.run(host='0.0.0.0', port=5019, debug=True)