Tour Booking Backend (generated from attendance project)
- FastAPI + SQLModel + MySQL (aiomysql)
- Endpoints: /tours (GET, POST, DELETE), /auth (register/login), /users/me (dev admin check)
- Use .env to configure DATABASE_URL
- To create dev admin: python -m app.dev.create_admin (or run inside container)
