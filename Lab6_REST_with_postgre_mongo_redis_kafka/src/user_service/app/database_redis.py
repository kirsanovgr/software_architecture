import redis

redis_client = redis.Redis(host='cash_db', port=6379, decode_responses=True)
