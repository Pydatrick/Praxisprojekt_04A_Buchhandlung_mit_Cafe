from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

app = FastAPI(title       = "Bookstore/Coffee_Shop-API",
              description = "Provides bookstore and coffee_shop database control",
              version     = "0.9.2"
             )

# bookstore routes
from routers.bookstore import books, ebooks, movies, summary, bookstore_logs
app.include_router(books.router,   prefix = "/bookstore/books",   tags = ["Books"])
app.include_router(ebooks.router,  prefix = "/bookstore/ebooks",  tags = ["Ebooks"])
app.include_router(movies.router,  prefix = "/bookstore/movies",  tags = ["Movies"])
app.include_router(summary.router, prefix = "/bookstore/summary", tags = ["Summary"])
app.include_router(bookstore_logs.router, prefix = "/bookstore/logs", tags = ["Bookstore logs"])

# coffee_shop routes
from routers.coffee_shop import americano, apple_spritzer, backstock, latte, lemonade, coffee_shop_logs
app.include_router(backstock.router,  prefix = "/coffee_shop/backstock",  tags = ["Backstock"])
app.include_router(latte.router,      prefix = "/coffee_shop/latte",      tags = ["Latte"])
app.include_router(americano.router,  prefix = "/coffee_shop/americano",  tags = ["Americano"])
app.include_router(lemonade.router,   prefix = "/coffee_shop/lemonade",   tags = ["Lemonade"])
app.include_router(apple_spritzer.router,   prefix = "/coffee_shop/apple_spritzer",  tags = ["Apple spritzer"])
app.include_router(coffee_shop_logs.router, prefix = "/coffee_shop/logs", tags = ["Coffee shop logs"])

# Favicon
@app.get("/favicon.ico")
def favicon():
    return FileResponse(ROOT_DIR / 'static' / 'favicon.ico', media_type = "image/vnd.microsoft.icon")

# app starten
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",
                host         = "localhost",
                port         = 58723,
                reload       = True,
                # Falls keine ssl Zertifikate zur Hand auskommentieren:
                ssl_certfile = ROOT_DIR / 'sql' / 'data' / 'secret' / 'cert.pem',
                ssl_keyfile  = ROOT_DIR / 'sql' / 'data' / 'secret' / 'key.pem'
                )