import requests
from ext import app, db
from models import Game

CUSTOM_GAMES = [
    {"title": "GTA V", "genre": "Action", "price": "$29.99", "store": "Steam",
     "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/271590/header.jpg",
     "link": "https://store.steampowered.com/app/271590/", "description": "Rockstar's legendary open world game."},
    {"title": "Red Dead Redemption 2", "genre": "Action", "price": "$59.99", "store": "Steam",
     "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1174180/header.jpg",
     "link": "https://store.steampowered.com/app/1174180/",
     "description": "Epic tale of life in America’s unforgiving heartland."},
    {"title": "Cyberpunk 2077", "genre": "RPG", "price": "$39.99", "store": "Steam",
     "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1091500/header.jpg",
     "link": "https://store.steampowered.com/app/1091500/",
     "description": "An open-world, action-adventure RPG set in Night City."},
    {"title": "Elden Ring", "genre": "RPG", "price": "$39.99", "store": "Steam",
     "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1245620/header.jpg",
     "link": "https://store.steampowered.com/app/1245620/", "description": "Brandish the power of the Elden Ring."},
    {"title": "Minecraft", "genre": "Sandbox", "price": "$26.95", "store": "Mojang",
     "img": "/static/images/minecraft.jpg", "link": "https://www.minecraft.net/",
     "description": "Explore infinite worlds and build everything."},
    {"title": "Valorant", "genre": "FPS", "price": "Free", "store": "Riot Games", "img": "/static/images/valorant.jpg",
     "link": "https://playvalorant.com/", "description": "A 5v5 character-based tactical shooter."},
    {"title": "League of Legends", "genre": "MOBA", "price": "Free", "store": "Riot Games",
     "img": "/static/images/lol.jpg", "link": "https://www.leagueoflegends.com/",
     "description": "A team-based strategy game."},
    {"title": "Terraria", "genre": "Sandbox", "price": "$9.99", "store": "Steam",
     "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/105600/header.jpg",
     "link": "https://store.steampowered.com/app/105600/", "description": "Dig, Fight, Explore, Build!"},
    {"title": "Counter-Strike 2", "genre": "FPS", "price": "Free", "store": "Steam",
     "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/730/header.jpg",
     "link": "https://store.steampowered.com/app/730/", "description": "The next chapter in the CS saga."},
    {"title": "Far Cry 5", "genre": "FPS", "price": "$29.99", "store": "Steam",
     "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/552520/header.jpg",
     "link": "https://store.steampowered.com/app/552520/", "description": "Welcome to Hope County, Montana."},
    {"title": "Resident Evil 4", "genre": "Action", "price": "$49.99", "store": "Steam",
     "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2050650/header.jpg",
     "link": "https://store.steampowered.com/app/2050650/", "description": "Survival is just the beginning."},
    {"title": "Ghost of Tsushima", "genre": "Action", "price": "$49.99", "store": "Steam",
     "img": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/2215430/header.jpg",
     "link": "https://store.steampowered.com/app/2215430/", "description": "Experience feudal Japan like never before."}
]
with app.app_context():
    db.drop_all()
    db.create_all()

    for g in CUSTOM_GAMES:
        game = Game(title=g["title"], genre=g["genre"], img=g["img"], rating="4.8/5", price=g["price"], store=g["store"], link=g["link"], description=g["description"])
        db.session.add(game)

    try:
        response = requests.get("https://www.freetogame.com/api/games")
        api_data = response.json()
        for g in api_data[:12]:
            if not any(custom["title"].lower() == g["title"].lower() for custom in CUSTOM_GAMES):
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
        print(f"API fetch skipped or failed: {e}")

    db.session.commit()
    print("Database successfully synchronized with both sets of games!")