from app import *

with app.app_context():
   # db.drop_all()

   db.create_all()
   # Project.__table__.drop(bind=db.engine)
   # user = User(name='John2', username = 'jvvfdohn222', password = '23232')
   # db.session.add(user)
   # db.session.commit()
   # project = Project(title='testTitle', description = 'Наша мета — випустити додаток, який завоює ринок! А по дорозі — просто отримати задоволення. Цікавих завдань море: від розробки зручного трекера звичок до автоматичного виявлення спаму в соцмережах.', user_id = user.id)
   # db.session.add(project)
   # db.session.commit()
   # users = User.query.all()
   # print(users)