from redis import Redis

from core import config


redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def main():
    print(redis.ping())
    redis.set("name", "yaros")
    redis.set("foo", "bar")
    redis.set("number", "42")
    print("name:", redis.get("name"))
    print(
        [
            redis.get("name"),
            redis.get("foo"),
            redis.get("spam"),
        ]
    )
    redis.getdel("foo")


if __name__ == "__main__":
    main()
