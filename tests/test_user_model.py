import time
import unittest
from datetime import datetime

from app import create_app, db
from app.models import AnonymousUser, Permission, Role, User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app.config["SECRET_KEY"] = "Secret value"
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password="cat")
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password="cat")
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password="cat")
        self.assertTrue(u.verify_password("cat"))
        self.assertFalse(u.verify_password("dog"))

    def test_password_salts_are_random(self):
        u = User(password="cat")
        u2 = User(password="cat")
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password="cat")
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(password="cat")
        u2 = User(password="dog")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password="cat")
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_token(self):
        u = User(password="cat", username="Jorge")
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(User.reset_password(token, "dog"))
        self.assertTrue(u.verify_password("dog"))

    def test_invalid_reset_token(self):
        u = User(password="cat")
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token + "a", "horse"))
        self.assertTrue(u.verify_password("cat"))

    def test_valid_email_change_token(self):
        u = User(email="john@example.com", password="cat")
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token("susan@example.org")
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == "susan@example.org")

    def test_invalid_email_change_token(self):
        u1 = User(email="john@example.com", password="cat")
        u2 = User(email="susan@example.org", password="dog")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_email_change_token("david@example.net")
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == "susan@example.org")

    def test_duplicate_email_change_token(self):
        u1 = User(email="john@example.com", password="cat")
        u2 = User(email="susan@example.org", password="dog")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u2.generate_email_change_token("john@example.com")
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == "susan@example.org")

    def test_user_role(self):
        u = User(email="john@example.com", password="cat")
        self.assertTrue(u.can(Permission.VIEW))
        self.assertFalse(u.can(Permission.EDIT))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_moderator_role(self):
        r = Role.query.filter_by(name="Editor").first()
        u = User(email="john@example.com", password="cat", role=r)
        self.assertTrue(u.can(Permission.EDIT))
        self.assertTrue(u.can(Permission.VIEW))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_administrator_role(self):
        r = Role.query.filter_by(name="Administrator").first()
        u = User(email="john@example.com", password="cat", role=r)
        self.assertTrue(u.can(Permission.EDIT))
        self.assertTrue(u.can(Permission.VIEW))
        self.assertTrue(u.can(Permission.ADD))
        self.assertTrue(u.can(Permission.ADMIN))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.EDIT))
        self.assertFalse(u.can(Permission.VIEW))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_timestamps(self):
        u = User(password="cat")
        db.session.add(u)
        db.session.commit()
        self.assertTrue((datetime.utcnow() - u.member_since).total_seconds() < 3)
        self.assertTrue((datetime.utcnow() - u.last_seen).total_seconds() < 3)

    def test_ping(self):
        u = User(password="cat")
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.last_seen
        u.ping()
        self.assertTrue(u.last_seen > last_seen_before)

    def test_gravatar(self):
        u = User(email="john@example.com", password="cat")
        with self.app.test_request_context("/"):
            gravatar = u.gravatar()
            gravatar_256 = u.gravatar(size=256)
            gravatar_pg = u.gravatar(rating="pg")
            gravatar_retro = u.gravatar(default="retro")
        self.assertTrue(
            "https://secure.gravatar.com/avatar/" + "d4c74594d841139328695756648b6bd6"
            in gravatar
        )
        self.assertTrue("s=256" in gravatar_256)
        self.assertTrue("r=pg" in gravatar_pg)
        self.assertTrue("d=retro" in gravatar_retro)

    # def test_to_json(self):
    #     u = User(email='john@example.com', password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     with self.app.test_request_context('/'):
    #         json_user = u.to_json()
    #     expected_keys = ['url', 'username', 'member_since', 'last_seen',
    #                      'posts_url']
    #     self.assertEqual(sorted(json_user.keys()), sorted(expected_keys))
    #     self.assertEqual('/api/v1/users/' + str(u.id), json_user['url'])
