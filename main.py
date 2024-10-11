import os

from dotenv import load_dotenv

from services.instagram import InstagramService

if __name__ == "__main__":
    load_dotenv()
    login = os.environ.get("LOGIN")
    password = os.environ.get("PASSWORD")
    target = os.environ.get("TARGET")
    followers_count = int(os.environ.get("FOLLOWERS_COUNT", 50))
    service = InstagramService(login, password, target, followers_count)
    result = service.parse()
    service.save()
    print(service.result)
