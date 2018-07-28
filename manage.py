from app import initApp
from config import DevConfig

app = initApp()
app.config.from_object(DevConfig)
