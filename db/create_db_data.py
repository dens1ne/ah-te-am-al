from data import db_session
from data.users import User
from data.jobs import Job as Jobs

db_session.global_init('database.db')
db_sess = db_session.create_session()

# users_data = [
#         ('Scott', 'Ridley', 21, 'captain', 'research engineer', 'module_1', 'scott_chief@mars.org'),
#         ('Dorvard', 'Kventin', 18, 'crewmate', 'astronaut', 'module_1', 'dorvard_crew@mars.org'),
#         ('Croft', 'Lara', 20, 'crewmate', 'scientist', 'module_1', 'croft_science@mars.org'),
#         ('Logi', 'Tech', 25, 'crewmate', 'engineer', 'module_1', 'logi_tech__@mars.org')
# ]
#
# for surname, name, age, position, speciality, address, email in users_data:
#     user = User()
#     user.surname = surname
#     user.name = name
#     user.age = age
#     user.position = position
#     user.speciality = speciality
#     user.address = address
#     user.email = email
#     db_sess.add(user)
#     db_sess.commit()
#
# job = Job()
# job.team_leader_id = 1
# job.job = 'deployment of residential modules 1 and 2'
# job.work_size = 15
# job.collaborators = '2,3'
# db_sess.add(job)
# db_sess.commit()

members = db_sess.query(User).filter(User.address == 'module_1', User.age < 21).all()

for member in members:
    member.address = 'module_3'

db_sess.commit()
