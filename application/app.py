from flask import Flask, render_template
from search import search
from item_submission import item_bp

app = Flask(__name__, static_folder='./public', template_folder='./html')
#mysql = MySQL(app)

# Register the Blueprint with the app
app.register_blueprint(search, url_prefix="")
app.register_blueprint(item_bp, url_prefix="")


@app.route('/index.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about/About.html')

@app.route('/about/Justin.html')
def justin():
    return render_template('about/Justin.html')

@app.route('/about/Douglas.html')
def douglas():
    return render_template('about/Douglas.html')

@app.route('/about/GioJung.html')
def giojung():
    return render_template('about/GioJung.html')

@app.route('/about/Gurpreet.html')
def gurpreet():
    return render_template('about/Gurpreet.html')

@app.route('/about/Gursimran.html')
def gursimran():
    return render_template('about/Gursimran.html')

@app.route('/about/Omar.html')
def omar():
    return render_template('about/Omar.html')

@app.route('/about/Sell.html')
def sell():
    return render_template('about/Sell.html')
#@app.route('/about/Search.html')
#def search_page():
#    return render_template('about/Search.html')

#@app.route("/livesearch",methods=["POST","GET"])
#def livesearch():
#    searchbox = request.form.get("text")
#    cursor = mysql.connection.cursor()
#    query = "SELECT p.* FROM Product p JOIN ProductCategory pc ON p.ProductID = pc.ProductID JOIN Category c ON pc.CategoryID = c.CategoryID WHERE c.Name = %s AND (p.Title LIKE %s OR p.Description LIKE %s)"
#    cursor.execute(query)
#    result = cursor.fetchall()
#    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
