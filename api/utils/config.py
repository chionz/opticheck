import os
from jinja2 import Environment, FileSystemLoader

# Define your JWT secret and algorithm
SECRET_KEY = os.getenv("SECRET_KEY", "MY SECRET KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
templates_env = Environment(loader=FileSystemLoader("templates"))
