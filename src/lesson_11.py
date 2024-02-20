from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Post:
    message: str
    timestamp: datetime


class SocialChannel(ABC):
    def __init__(self, number_of_followers: int):
        self.number_of_followers = number_of_followers

    @abstractmethod
    def make_post(self, post: Post):
        ...


class YouTube(SocialChannel):
    def make_post(self, post: Post):
        print(f"YouTube: {post}")


class Facebook(SocialChannel):
    def make_post(self, post: Post):
        print(f"Facebook: {post}")


class Twitter(SocialChannel):
    def make_post(self, post: Post):
        print(f"Twitter: {post}")


def process_schedule(posts: list[Post], channels: list[SocialChannel]) -> None:
    for post in posts:
        for channel in channels:
            if post.timestamp <= datetime.now():
                channel.make_post(post)


channel_list = [
    YouTube(56),
    Facebook(13),
    Twitter(3),
]

post_list = [
    Post(message='Hello, everybody', timestamp=datetime.now() - timedelta(days=1)),
    Post(message='Bye, everybody', timestamp=datetime.now() + timedelta(days=1)),

]

process_schedule(post_list, channel_list)
