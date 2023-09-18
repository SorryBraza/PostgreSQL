import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE
            );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES client(id),
                phone VARCHAR(12) UNIQUE
            );
            """)
        conn.commit() 
    pass

def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        data = (first_name, last_name, email)
        cur.execute("""
            INSERT INTO client(first_name, last_name, email) VALUES (%s, %s, %s);
            """, data)
        conn.commit() 
    pass

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        data = (client_id, phone)
        cur.execute("""
            INSERT INTO phones(client_id, phone) VALUES (%s, %s);
            """, data)
        conn.commit() 
    pass

def change_client(conn, client_id):
    with conn.cursor() as cur:
        num = input(f'Уточните, какие данные хотите изменить? (1 - Имя, 2 - Фамилия, 3 - e-mail)\nВаш ответ: ')
        while True:
            if num == '1':
                first_name = input(f'Введите новое имя: ')
                cur.execute("""
                    UPDATE client SET first_name=%s WHERE id=%s;
                    """, (first_name, client_id))
                conn.commit() 
                break
            elif num == '2':
                last_name = input(f'Введите новую фамилию: ')
                cur.execute("""
                    UPDATE client SET last_name=%s WHERE id=%s;
                    """, (last_name, client_id))
                conn.commit() 
                break
            elif num == '3':
                email = input(f'Введите новый email: ')
                cur.execute("""
                    UPDATE client SET email=%s WHERE id=%s;
                    """, (email, client_id))
                conn.commit() 
                break
            else:
                num = input(f'Уточните, какие данные хотите изменить? (1 - Имя, 2 - Фамилия, 3 - e-mail)\nВаш ответ: ')
    pass

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        data = (client_id, phone)
        cur.execute("""
            DELETE FROM phones WHERE client_id=%s AND phone=%s;
        """, (data))
        conn.commit() 
    pass

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phones WHERE client_id=%s;
        """, (client_id,))
        cur.execute("""
            DELETE FROM client WHERE id=%s;
        """, (client_id,))
        conn.commit() 
    pass

def find_client(conn):
    with conn.cursor() as cur:
        num = input(f'Уточните, по каким данным нужно найти клиента? (1 - Имя, 2 - Фамилия, 3 - e-mail, 4 - телефон)\nВаш ответ: ')
        while True:
            if num == '1':
                first_name = input(f'Введите имя: ')
                cur.execute("""
                    SELECT first_name, last_name, email, phone FROM client AS c LEFT JOIN phones AS p on c.id = p.client_id WHERE first_name=%s;
                    """, (first_name,))
                data = cur.fetchall()
                if data != []:
                    print(data)
                else:
                    print('Ничего не найдено')
                break
            elif num == '2':
                last_name = input(f'Введите фамилию: ')
                cur.execute("""
                    SELECT first_name, last_name, email, phone FROM client AS c LEFT JOIN phones AS p on c.id = p.client_id WHERE last_name=%s;
                    """, (last_name,))
                data = cur.fetchall()
                if data != []:
                    print(data)
                else:
                    print('Ничего не найдено')
                break
            elif num == '3':
                email = input(f'Введите email: ')
                cur.execute("""
                    SELECT first_name, last_name, email, phone FROM client AS c LEFT JOIN phones AS p on c.id = p.client_id WHERE email=%s;
                    """, (email,))
                data = cur.fetchall()
                if data != []:
                    print(data)
                else:
                    print('Ничего не найдено')
                break
            elif num == '4':
                phone = input(f'Введите телефон: ')
                cur.execute("""
                    SELECT first_name, last_name, email, phone FROM client AS c LEFT JOIN phones AS p on c.id = p.client_id 
                        WHERE c.id = (SELECT client_id FROM phones WHERE phone=%s);
                    """, (phone,))
                data = cur.fetchall()
                if data != []:
                    print(data)
                else:
                    print('Ничего не найдено')
                break
            else:
                num = input(f'Уточните, по каким данным нужно найти клиента? (1 - Имя, 2 - Фамилия, 3 - e-mail, 4 - телефон)\nВаш ответ: ')
    pass


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    create_db(conn)
    add_client(conn, 'Ivan', 'Ivanov', 'ivan@mail.ru')
    add_phone(conn, 1, '+79005005021')
    add_phone(conn, 1, '+79005005022')
    change_client(conn, 1)
    delete_phone(conn, 1, '+79005005022')
    delete_client(conn, 1)
    find_client(conn)
    pass  # вызывайте функции здесь

conn.close()