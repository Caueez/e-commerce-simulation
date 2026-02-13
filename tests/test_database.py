async def test_database():
    import os

    os.system("clear")

    from typing import Optional
    import asyncpg

    from infra.database.postgres.postgres import PostgresDatabase
    from infra.database.repository import DatabaseRepository

    try:
        print("Iniciando teste de conexão com o banco de dados...")

        repo = DatabaseRepository(PostgresDatabase("localhost", 5432, "admin", "admin", "db"))

        await repo.connect()

        await repo.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            );
            """
        )
        print("Tabela users criada com sucesso")

        print("Iniciando cadastro de usuário...")

        name = str(input("Digite o nome do usuário: "))
        email = str(input("Digite o email do usuário: "))
        password = str(input("Digite a senha do usuário: "))

        users : Optional[asyncpg.Record] = await repo.fetch_one(
            """
            SELECT * FROM users 
            WHERE email = $1
            """, email
        )

        if users:
            print("Email já cadastrado")

        else:
            await repo.execute(
                """
                INSERT INTO users (name, email, password) VALUES ($1, $2, $3);
                """, name, email, password
            )
            print("Usuário cadastrado com sucesso")

        user : Optional[asyncpg.Record] = await repo.fetch_one("SELECT * FROM users WHERE email = $1", email)
        if user: 
            print(f"{user.get("id")} -- {user.get("name")} -- {user.get("email")}")

    except KeyboardInterrupt as e:
        print(e)
    else:
        await repo.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_database())