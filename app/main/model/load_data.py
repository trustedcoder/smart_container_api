import os
from .. import db
from .users import User
from .containers import Containers
from ..helper.auth_methods import AuthMethod
from ..business.container_business import ContainerBusiness


def load_db_data():
    """ run all functions """
    #add_containers()
    ContainerBusiness.detect_object()


def add_containers():
    count = 0
    while 50 > count:
        public_id = ('\n'.join(map(str, AuthMethod.random_number(1, 2, 100000000000))))
        new_data = Containers(
            public_id=public_id,
            status=0
        )
        AuthMethod.save_changes(new_data)
        count = count+1
