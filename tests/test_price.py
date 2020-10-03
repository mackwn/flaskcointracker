
# Helpers
def userlogin(email,password,client):
    client.post('/login',data={
        'email':"{email}".format(email=email),
        'password':"{password}".format(password=password)
    }, follow_redirects=True)
    User = flaskcointracker.models.User
    user = User.query.filter_by(email=email).first()
    return user







@pytest.fixture
def client():
    # temporary db path and db file and rewrite cointracker db config
    db_fd, db_file = tempfile.mkstemp(suffix='.db')
    flaskcointracker.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{db_file}".format(db_file=db_file)
    # set testing config to true, overwriting config default
    flaskcointracker.app.config['TESTING'] = True
    flaskcointracker.app.config['WTF_CSRF_ENABLED'] = False
    flaskcointracker.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #flaskcointracker.app.config['SQLALCHEMY_DATABASE_URI'] = db_fd

    with flaskcointracker.app.test_client() as client:
        with flaskcointracker.app.app_context():
            #db_fd.create_all()
            #db = SQLalchemy(flaskcointracker.app)
            flaskcointracker.db.create_all()
            User = flaskcointracker.models.User
            user = User(email="testuser@test.com",password="testpass")
            flaskcointracker.db.session.add(user)
            user2 = User(email="testuser2@test.com",password="testpass")
            flaskcointracker.db.session.add(user2)
            flaskcointracker.db.session.commit()
            note = Notification(price=250,coin='btc-usd-coinbase',owner=User.query.first())
            note2 = Notification(price=250,coin='btc-usd-coinbase',owner=user2)
            flaskcointracker.db.session.add(note)
            flaskcointracker.db.session.add(note2)
            flaskcointracker.db.session.commit()
            user = User.query.first()
            print(user.notifications.first())
            print(len(user.notifications.all()))

        yield client
    flaskcointracker.db.session.remove()
    flaskcointracker.db.drop_all()
    os.close(db_fd)
    os.unlink(db_file)