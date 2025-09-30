# NFT Marketplace Backend

This is a backend for an NFT marketplace built with Django and Django REST Framework.  
It supports user registration, JWT authentication, and basic user management.

## Features

- Custom user model
- User registration endpoint
- JWT login and token refresh
- PostgreSQL database integration

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/LilitAsa/NFT-marketplace.git
   cd backend
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/scripts/activate  # On Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure your PostgreSQL database in `backend/settings.py`.

5. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Start the development server:
   ```
   python manage.py runserver

7. Open new terminal:
   ```
   cd frontend
   npm run dev
   ՝՝՝

## API 1Endpoints

- `POST /api/accounts/register/` — Register a new user
- `POST /api/accounts/login/` — Obtain JWT token
- `POST /api/accounts/token/refresh/` — Refresh JWT token

## License

MIT
