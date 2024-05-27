from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



def main():
    app.run(port=5000, debug=True)

if __name__=="__main__":
    main()