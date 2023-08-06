import random
import string
from enum import Enum

from husteblume import api


class AgeGroup(Enum):
    UP_TO_TWENTY = 'UP_TO_TWENTY'
    TWENTY_ONE_TO_FORTY = 'TWENTY_ONE_TO_FORTY'
    FORTY_ONE_AND_ABOVE = 'FORTY_ONE_AND_ABOVE'


class Gender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'


class User(object):
    appId: str = ""
    password: str = ""

    @staticmethod
    def register(age_group: AgeGroup, birth_month: int, gender: Gender, password: str = None):
        if password is None:
            password = ''.join(random.choice(string.ascii_letters) for i in range(26))

        r = api('post', 'https://api.husteblume-app.de/users', data=dict(
            age_group=age_group.value, birth_month=birth_month, gender=gender.value, pwd=password
        ))

        u = User(r.json()['appId'], password)
        return u

    def __repr__(self):
        return f"<User: appId={self.appId}>"

    def __init__(self, appId: str, password: str):
        self.appId = appId
        self.password = password
