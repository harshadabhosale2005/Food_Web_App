from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)

app.secret_key = "foodie_secret"

# DATABASE CONNECTION

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="foodie_db"
)

cursor = db.cursor()

# HOME PAGE

@app.route('/')
def home():
     return render_template('Bg page.html')

# LOGIN PAGE

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        sql = "SELECT * FROM users WHERE username=%s AND password=%s"

        values = (username, password)

        cursor.execute(sql, values)

        user = cursor.fetchone()

        if user:

            session['username'] = username

            return redirect('/')

        else:
            return "Invalid Credentials"

    return render_template('login.html')

# REGISTER PAGE

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password == confirm:

            sql = """
            INSERT INTO users
            (username, email, password)
            VALUES (%s, %s, %s)
            """

            values = (username, email, password)

            cursor.execute(sql, values)

            db.commit()

            return redirect('/login')

        else:
            return "Passwords Do Not Match"

    return render_template('register.html')

# LOGOUT

@app.route('/logout')
def logout():

    session.pop('username', None)

    return render_template('Bg page.html')

# MENU PAGE

@app.route('/menu')
def menu():
  return render_template('menu.html')

# VEG PAGE

@app.route('/veg')
def veg():

    if 'username' not in session:
        return redirect('/login')

    return render_template('veg.html')

# NON VEG PAGE

@app.route('/nonveg')
def nonveg():

    if 'username' not in session:
        return redirect('/login')

    return render_template('non veg.html')


#cust order
@app.route('/buy/<food>/<price>')
def buy(food, price):

    if 'username' not in session:
        return redirect('/login')

    return render_template(
        'confirm_order.html',
        food=food,
        price=price
    )


@app.route('/delivery', methods=['POST'])
def delivery():

    food = request.form['food']

    price = request.form['price']

    quantity = request.form['quantity']

    return render_template(

        'delivery.html',

        food=food,

        price=price,

        quantity=quantity

    )

@app.route('/place_order', methods=['POST'])
def place_order():

    if 'username' not in session:
        return redirect('/login')

    username = session['username']

    food = request.form['food']

    price = request.form['price']

    quantity = request.form['quantity']

    customer_name = request.form['customer_name']

    mobile = request.form['mobile']

    address = request.form['address']

    payment = request.form['payment']

    sql = """
    INSERT INTO customer_orders
    (username, food_name, price, quantity,
    customer_name, mobile,
    address, payment_method)

    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        username,
        food,
        price,
        quantity,
        customer_name,
        mobile,
        address,
        payment
    )

    cursor.execute(sql, values)

    db.commit()

    return """
    <div class='success-box'>

    <h1>🎉 Order Confirmed</h1>

    <h2>Your food will be delivered soon 🍔</h2>

    </div>
    """





#feedback page
@app.route('/feedback', methods=['POST'])
def feedback():

    if 'username' not in session:
        return redirect('/login')

    username = session['username']

    message = request.form['message']

    sql = """
    INSERT INTO feedback
    (name, message)
    VALUES (%s, %s)
    """

    values = (username, message)

    cursor.execute(sql, values)

    db.commit()

    return "Feedback Submitted Successfully"

# RUN APP

if __name__ == '__main__':
    app.run(debug=True)