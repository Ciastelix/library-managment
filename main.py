from fastapi import FastAPI
from app.routes import router
from app.containers import Container
import uvicorn

app = FastAPI()
container = Container()
db = container.db()
db.create_database()
app.container = container
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app)
