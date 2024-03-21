import redis
import os
from dotenv import load_dotenv

load_dotenv('.env')

redisClient = redis.Redis(
  host=os.getenv("REDIS_HOST"),
  port=os.getenv("REDIS_PORT"),
  password=os.getenv("REDIS_PASSWORD"))
