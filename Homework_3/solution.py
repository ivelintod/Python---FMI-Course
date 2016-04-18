import uuid
import math
import datetime
import functools
from collections import deque, defaultdict


class User:

    def __init__(self, full_name):
        self.full_name = full_name
        self.__uuid = uuid.uuid4()
        self.posts = deque([], 50)

    @property
    def uuid(self):
        return self.__uuid

    def add_post(self, post_content):
        date_time = datetime.datetime.now()
        self.posts.append(Post(self.uuid, date_time, post_content))

    def get_post(self):
        for i in range(self.posts.maxlen):
            yield self.posts[i]


class Post:

    def __init__(self, author, published_at, content):
        self.author = author
        self.published_at = published_at
        self.content = content


def user_checker_arg_modifier(arg_change=False):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args):
            new_args = []
            new_args.append(args[0])
            for arg in args[1:]:
                if not isinstance(arg, int) \
                   and arg not in args[0].uuid_to_users:
                    raise UserDoesNotExistError
                elif not isinstance(arg, int):
                    new_args.append(args[0].uuid_to_users[arg])
                elif isinstance(arg, int):
                    new_args.append(arg)
            if arg_change:
                return func(*new_args)
            return func(*args)
        return wrapper
    return deco


class SocialGraph:

    def __init__(self):
        self.users = set()
        self.uuid_to_users = dict()
        self.follows = defaultdict(set)
        self.followed_by = defaultdict(set)

    def add_user(self, user):
        if user in self.users:
            raise UserAlreadyExistsError
        self.users.add(user)
        self.uuid_to_users[user.uuid] = user

    @user_checker_arg_modifier()
    def get_user(self, user_uuid):
        return self.uuid_to_users[user_uuid]

    @user_checker_arg_modifier(True)
    def delete_user(self, user_uuid):
        self.users.remove(user_uuid)
        del self.uuid_to_users[user_uuid.uuid]

    @user_checker_arg_modifier()
    def follow(self, follower, followee):
        self.follows[follower].add(followee)
        self.followed_by[followee].add(follower)

    @user_checker_arg_modifier()
    def unfollow(self, follower, followee):
        try:
            self.follows[follower].remove(followee)
            self.followed_by[followee].remove(follower)
        except KeyError:
            pass

    @user_checker_arg_modifier()
    def is_following(self, follower, followee):
        return followee in self.follows[follower]

    @user_checker_arg_modifier()
    def followers(self, user_uuid):
        return self.followed_by[user_uuid]

    @user_checker_arg_modifier()
    def following(self, user_uuid):
        return self.follows[user_uuid]

    @user_checker_arg_modifier()
    def friends(self, user_uuid):
        return self.follows[user_uuid] & self.followed_by[user_uuid]

    def get_distances(self, user_uuid):
        visited = set()
        distances = defaultdict(set)
        queue = []
        queue.append((user_uuid, 0))

        while queue:
            current = queue[0][0]
            level = queue[0][1] + 1
            for followed in self.follows[current]:
                if followed not in distances:
                    distances[level].add(followed)
                if followed not in visited:
                    queue.append((followed, level))
                    visited.add(followed)
            queue.pop(0)

        return distances

    @user_checker_arg_modifier()
    def max_distance(self, user_uuid):
        if not self.follows[user_uuid]:
            return math.inf

        distances = self.get_distances(user_uuid)
        return max(distances.keys())

    @user_checker_arg_modifier()
    def min_distance(self, from_user_uuid, to_user_uuid):
        if not self.follows[from_user_uuid]:
            raise UsersNotConnectedError

        visited = set()
        queue = []
        queue.append((from_user_uuid, 0))

        while queue:
            current = queue[0][0]
            level = queue[0][1] + 1
            for followed in self.follows[current]:
                if followed == to_user_uuid:
                    return level
                if followed not in visited:
                    queue.append((followed, level))
                    visited.add(followed)
            queue.pop(0)
        else:
            raise UsersNotConnectedError

    @user_checker_arg_modifier()
    def nth_layer_followings(self, user_uuid, n):
        if not self.follows[user_uuid]:
            return set()

        distances = self.get_distances(user_uuid)
        try:
            return distances[n]
        except KeyError:
            return set()

    @user_checker_arg_modifier()
    def generate_feed(self, user_uuid, offset=0, limit=10):
        latest_posts = []
        for followed in self.follows[user_uuid]:
            latest_posts.extend(self.uuid_to_users[followed].posts)
        latest_posts.sort(key=lambda x: x.published_at)
        return latest_posts[offset + 1: offset + limit]


class UserAlreadyExistsError(Exception):
    pass


class UserDoesNotExistError(Exception):
    pass


class UsersNotConnectedError(Exception):
    pass


ivo = User('Ivo')
joro = User('Joro')
chepo = User('Chefo')
bobi = User('Bobi')
bogi = User('Bogi')
valio = User('Valio')
ivan = User('Ivan')
s = SocialGraph()
s.add_user(ivo)
s.add_user(joro)
s.add_user(chepo)
s.add_user(bobi)
s.add_user(bogi)
s.add_user(valio)
s.add_user(ivan)

s.follow(ivo.uuid, joro.uuid)
s.follow(ivo.uuid, chepo.uuid)
s.follow(joro.uuid, bobi.uuid)
s.follow(bobi.uuid, bogi.uuid)
#s.follow(joro.uuid, chepo.uuid)
s.follow(joro.uuid, valio.uuid)
s.follow(valio.uuid, chepo.uuid)
s.follow(chepo.uuid, ivan.uuid)
#s.follow(chepo.uuid, bogi.uuid)
