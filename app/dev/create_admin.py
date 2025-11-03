import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import AsyncSessionLocal
from app.models import User
from app.core.security import get_password_hash

async def main():
    async with AsyncSessionLocal() as session:
        admin = User(email='admin@example.com', full_name='Admin', hashed_password=get_password_hash('Test@123'), role='admin')
        session.add(admin)
        await session.commit()
        print('admin created')

if __name__ == '__main__':
    asyncio.run(main())
