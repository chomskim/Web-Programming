'''
Created on 2018. 8. 21.

@author: cskim
'''
# compare to quick_session.py - below in this gist - this version does NOT use session
# Therefore, it cannot pass variables to another route 

from flask import Flask

app = Flask(__name__)

new_user = 'OLD USER'
@app.route('/setuser/<user>')
def setuser(user):
    new_user = user
    return 'User value set to: ' + new_user


@app.route('/getuser')
def getuser():
    return 'User value was previously set to: ' + new_user


if __name__ == '__main__':
    app.run(port=5001, debug=True)