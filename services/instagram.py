import sqlite3
import instaloader


class InstagramService:
    def __init__(self, login: str, password: str, target: str, followers_count: int):
        self.loader = instaloader.Instaloader()
        self.loader.login(login, password)
        self.target = target
        self.followers_count = followers_count
        self.result = []

    def _create_db(self) -> sqlite3.Connection:
        connection = sqlite3.connect(f'{self.target.replace(".", "_")}.db')
        return connection

    def _create_table(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
        cursor.execute('''CREATE TABLE IF NOT EXISTS report (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    username TEXT NOT NULL,
                                    subscribers_count INTEGER,
                                    subscriptions_count INTEGER,
                                    post_count INTEGER
                                )''')
        connection.commit()

    def _save_result(self, cursor: sqlite3.Cursor) -> None:
        for item in self.result:
            cursor.execute('''INSERT INTO report (username, subscribers_count, subscriptions_count, post_count) 
                                  VALUES (?, ?, ?, ?)''', (
                item.get("username"), item.get("subscribers_count"), item.get("subscriptions_count"),
                item.get("post_count")))

    def _parse_follower(self, profile: instaloader.Profile) -> None:
        iteration = 0
        for follower in profile.get_followers():
            if iteration >= self.followers_count:
                return None
            self.result.append(
                {
                    'username': follower.username,
                    'subscribers_count': follower.followers,
                    'subscriptions_count': follower.followees,
                    'post_count': follower.mediacount
                }
            )
        return None

    def parse(self) -> list:
        profile = instaloader.Profile.from_username(self.loader.context, self.target)
        self._parse_follower(profile)
        return self.result

    def save(self) -> None:
        connection = self._create_db()
        cursor = connection.cursor()
        self._create_table(connection, cursor)
        self._save_result(cursor)
        connection.commit()
        connection.close()
