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


@app.route("/login", methods=["GET", "POST"])
def login():
    games = Game.query.all()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session["user"] = user.username
            return redirect("/")
        else:
            return render_template("login.html", games=games, error="Invalid username or password.")
    return render_template("login.html", games=games)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            form.username.errors.append("Username already taken, choose another.")
            return render_template("register.html", form=form)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(
            username=form.username.data,
            password=hashed_password,
            gender=form.gender.data
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    return render_template("register.html", form=form)


@app.route("/cart")
def cart():
    cart = session.get("cart", {})
    items = []
    total = 0
    all_games = Game.query.all()
    for game_id, qty in cart.items():
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
        results = [g for g in games if query.lower() in g.title.lower()]
    else:
        results = []
    return render_template("search.html", results=results, query=query, games=games)


@app.route("/game/<int:game_id>")
def game_details(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template("game_details.html", game=game)


@app.route("/free-games")
def free_games():
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


@app.route("/seed-db-now-secret123")
def seed_db():
    import requests

    Game.query.delete()
    db.session.commit()

    CUSTOM_GAMES = [
        {"title": "GTA V", "genre": "Action", "price": "$29.99", "store": "Steam", "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/271590/header.jpg", "link": "https://store.steampowered.com/app/271590/", "description": "Rockstar's legendary open world game."},
        {"title": "Red Dead Redemption 2", "genre": "Action", "price": "$59.99", "store": "Steam", "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1174180/header.jpg", "link": "https://store.steampowered.com/app/1174180/", "description": "Epic tale of life in America's unforgiving heartland."},
        {"title": "Cyberpunk 2077", "genre": "RPG", "price": "$39.99", "store": "Steam", "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/header.jpg", "link": "https://store.steampowered.com/app/1091500/", "description": "An open-world, action-adventure RPG set in Night City."},
        {"title": "Elden Ring", "genre": "RPG", "price": "$39.99", "store": "Steam", "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1245620/header.jpg", "link": "https://store.steampowered.com/app/1245620/", "description": "Brandish the power of the Elden Ring."},
        {"title": "Minecraft", "genre": "Sandbox", "price": "$26.95", "store": "Mojang", "img": "/static/images/minecraft.jpg", "link": "https://www.minecraft.net/", "description": "Explore infinite worlds and build everything."},
        {"title": "Valorant", "genre": "FPS", "price": "Free", "store": "Riot Games", "img": "/static/images/valorant.jpg", "link": "https://playvalorant.com/", "description": "A 5v5 character-based tactical shooter."},
        {"title": "League of Legends", "genre": "MOBA", "price": "Free", "store": "Riot Games", "img": "/static/images/lol.jpg", "link": "https://www.leagueoflegends.com/", "description": "A team-based strategy game."},
        {"title": "Terraria", "genre": "Sandbox", "price": "$9.99", "store": "Steam", "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/105600/header.jpg", "link": "https://store.steampowered.com/app/105600/", "description": "Dig, Fight, Explore, Build!"},
        {"title": "Counter-Strike 2", "genre": "FPS", "price": "Free", "store": "Steam", "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/730/header.jpg", "link": "https://store.steampowered.com/app/730/", "description": "The next chapter in the CS saga."},
        {"title": "Far Cry 5", "genre": "FPS", "price": "$29.99", "store": "Steam", "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/552520/header.jpg", "link": "https://store.steampowered.com/app/552520/", "description": "Welcome to Hope County, Montana."},
        {"title": "Resident Evil 4", "genre": "Action", "price": "$49.99", "store": "Steam", "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2050650/header.jpg", "link": "https://store.steampowered.com/app/2050650/", "description": "Survival is just the beginning."},
        {"title": "Ghost of Tsushima", "genre": "Action", "price": "$49.99", "store": "Steam", "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2215430/header.jpg", "link": "https://store.steampowered.com/app/2215430/", "description": "Experience feudal Japan like never before."}
    ]

    for g in CUSTOM_GAMES:
        game = Game(title=g["title"], genre=g["genre"], img=g["img"], rating="4.8/5",
                    price=g["price"], store=g["store"], link=g["link"], description=g["description"])
        db.session.add(game)

    try:
        response = requests.get("https://www.freetogame.com/api/games", timeout=10)
        api_data = response.json()
        for g in api_data[:12]:
            if not any(c["title"].lower() == g["title"].lower() for c in CUSTOM_GAMES):
                game = Game(
                    title=g["title"],
                    genre=g["genre"],
                    img=g["thumbnail"],
                    rating="4.2/5",
                    price="Free",
                    store=g["platform"],
                    link=g["freetogame_profile_url"],
                    description=g.get("short_description", "No description available.")
                )
                db.session.add(game)
    except Exception as e:
        print(f"API fetch failed: {e}")

    db.session.commit()
    return "Games seeded successfully!"


@app.route("/admin-users-secret123")
def admin_users():
    users = User.query.all()
    result = "<h2>Registered Users</h2><table border='1'><tr><th>ID</th><th>Username</th><th>Gender</th></tr>"
    for u in users:
        result += f"<tr><td>{u.id}</td><td>{u.username}</td><td>{u.gender}</td></tr>"
    result += "</table>"
    return result