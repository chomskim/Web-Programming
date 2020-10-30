from flask import Flask
app = Flask(__name__)
@app.route("/")
def index():
    return """<!DOCTYPE html>
<html>
  <head> 
    <title>My Page Title</title>
  </head>
  <body>
    <h1>Hello World!</h1>
  </body>
</html>"""
@app.route("/hi")
def hi():
    return """<!DOCTYPE html>
<html>
  <head> 
    <title>My Page Title</title>
  </head>
  <body>
    <h1>Hi, There!</h1>
  </body>
</html>"""
if __name__ == '__main__':
    app.run(port=5000, debug=True)
