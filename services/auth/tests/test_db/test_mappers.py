from auth.db.repositories import UserRepository, RoleRepository
from auth.models import User, Role


def test_user_mapper_works(db_session):
    db_session.execute("""
        INSERT INTO roles (id, name) VALUES
            (1, 'admin'),
            (2, 'developer')
    """)
    db_session.execute("""
        INSERT INTO users (id, name, email, password, public_id) VALUES
            (1, 'a', 'a', 'a', '1'),
            (2, 'b', 'b', 'b', '2')
    """)
    db_session.execute("""
       INSERT INTO user_to_role (user_id, role_id) VALUES
           (1, 1),
           (2, 1),
           (2, 2)
    """)
    role_1 = Role(name="admin")
    role_2 = Role(name="developer")

    user_1 = User(
        name="a",
        email="a",
        password="a",
        public_id="1",
        hash_password=False
    )
    user_1.roles = [role_1]

    user_2 = User(
        name="b",
        email="b",
        password="b",
        public_id="2",
        hash_password=False
    )
    user_2.roles = [role_1, role_2]

    expected_users = [user_1, user_2]

    user_repo = UserRepository(db_session)
    users = user_repo.list()

    print(users[0].__dict__)
    print(expected_users[0].__dict__)
    print(users[1].__dict__)
    print(expected_users[1].__dict__)
    assert users == expected_users


def test_user_mapper_add_role(db_session):
    db_session.execute("""
            INSERT INTO roles (id, name) VALUES
                (1, 'admin'),
                (2, 'developer')
        """)
    db_session.execute("""
            INSERT INTO users (id, name, email, password, public_id) VALUES
                (1, 'a', 'a', 'a', '1'),
                (2, 'b', 'b', 'b', '2')
        """)
    db_session.execute("""
           INSERT INTO user_to_role (user_id, role_id) VALUES
               (1, 1),
               (2, 1)
        """)

    user_repo = UserRepository(db_session)
    role_repo = RoleRepository(db_session)

    role_1 = role_repo.get(name="admin")
    role_2 = role_repo.get(name="developer")

    user_a = user_repo.get(email="a")
    user_a.roles.append(role_2)
    db_session.commit()

    user = user_repo.get(email="a")
    assert user.roles == [role_1, role_2]


def test_user_mapper_delete_role(db_session):
    db_session.execute("""
            INSERT INTO roles (id, name) VALUES
                (1, 'admin'),
                (2, 'developer')
        """)
    db_session.execute("""
            INSERT INTO users (id, name, email, password, public_id) VALUES
                (1, 'a', 'a', 'a', '1'),
                (2, 'b', 'b', 'b', '2')
        """)
    db_session.execute("""
           INSERT INTO user_to_role (user_id, role_id) VALUES
               (1, 1),
               (2, 1),
               (2, 2)
        """)

    user_repo = UserRepository(db_session)
    role_repo = RoleRepository(db_session)

    role_1 = role_repo.get(name="admin")
    role_2 = role_repo.get(name="developer")

    user_b = user_repo.get(email="b")
    user_b.roles.remove(role_2)
    db_session.commit()

    user = user_repo.get(email="b")
    assert user.roles == [role_1]
