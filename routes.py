from ext import app, db, bcrypt
from flask import render_template, redirect, session, request, abort
from forms import RegisterForm
from models import User, Game
from os import path

profiles = []


@app.route("/")
def home():
    games = Game.query.all()
    return render_template("main.html", games=games)


@app.route("/about")
def about():
    games = Game.query.all()
    return render_template("about.html", games=games)


@app.route("/login")
def login():
    games = Game.query.all()
    return render_template("login.html", games=games)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(
            username=form.username.data,
            password=hashed_password,
            gender=form.gender.data
        )
        db.session.add(new_user)
        db.session.commit()
        print("NEW USER REGISTERED:", new_user.username)
        return redirect("/")
    return render_template("register.html", form=form)


@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    items = []
    total = 0
    all_games = Game.query.all()

    for game_id, qty in cart.items():
        # Using dot notation (.id) because 'g' is a database object now
        game = next((g for g in all_games if str(g.id) == game_id), None)
        if game:
            if game.price != "Free":
                price = float(game.price.replace("$", ""))
                subtotal = price * qty
                total += subtotal
            else:
                subtotal = 0
            items.append({"game": game, "qty": qty, "subtotal": subtotal})

    return render_template("cart.html", games=all_games, items=items, total=total)


@app.route("/add-to-cart/<int:game_id>")
def add_to_cart(game_id):
    cart = session.get("cart", {})
    key = str(game_id)
    if key not in cart:
        cart[key] = 1
    else:
        cart[key] += 1
    session["cart"] = cart
    return redirect(request.referrer or "/")


@app.route("/remove-from-cart/<int:game_id>")
def remove_from_cart(game_id):
    cart = session.get("cart", {})
    key = str(game_id)
    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            del cart[key]
    session["cart"] = cart
    return redirect("/cart")


@app.route("/clear-cart")
def clear_cart():
    session.pop("cart", None)
    return redirect("/cart")


@app.route("/forgot_password")
def forgot_password():
    games = Game.query.all()
    return render_template("forgot_ur_password.html", games=games)


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    games = Game.query.all()
    if query:
        # Filter database objects using dot notation .title
        results = [g for g in games if query.lower() in g.title.lower()]
    else:
        results = []
    return render_template("search.html", results=results, query=query, games=games)


@app.route("/game/<int:game_id>")
def game_details(game_id):
    # Fetch specific game directly from database by its ID primary key
    game = Game.query.get_or_404(game_id)
    return render_template("game_details.html", game=game)


@app.route("/free-games")
def free_games():
    # Let the database do the filtering instead of standard lists!
    free = Game.query.filter_by(price="Free").all()
    return render_template("free_games.html", games=free)


@app.route("/rpg-games")
def rpg_games():
    rpg = Game.query.filter_by(genre="RPG").all()
    return render_template("rpg_games.html", games=rpg)


@app.route("/fps-games")
def fps_games():
    fps = Game.query.filter(Game.genre.like("%Shooter%")).all() or Game.query.filter_by(genre="FPS").all()
    return render_template("fps_games.html", games=fps)
