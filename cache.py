import redis
import os
from dotenv import load_dotenv

load_dotenv('.env')

redisClient = redis.Redis(
  host='redis-15645.c301.ap-south-1-1.ec2.cloud.redislabs.com',
  port=15645,
  password=os.getenv("REDIS_PASSWORD"))
