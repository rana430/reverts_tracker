import sqlite3

connection = sqlite3.connect('reverts_database.db')
cursor = connection.cursor()
cursor.execute(
    '''
    create table if not exists members(
        id int primary key,
        member_id int not null,
        member_name text not null,
        gender text not null,
        author text not null,
        date text not null,
        notes text
    )
    ''')
connection.commit()

connection.close()