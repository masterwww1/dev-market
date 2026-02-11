"""Utility script to create a user in the database."""
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from be.database import get_db_session
from be.models.user import User
from be.utils.password import hash_password


def create_user(email: str, password: str, status: str = "ACTIVE"):
    """Create a user in the database."""
    with get_db_session() as db:
        # Check if user already exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"User {email} already exists!")
            return

        user = User(
            email=email,
            password_hash=hash_password(password),
            active=True,
            status=status,
        )
        db.add(user)
        db.commit()
        print(f"User {email} created successfully!")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_user.py <email> <password> [status]")
        print("Example: python create_user.py admin@b2bmarket.com password123 ACTIVE")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    status = sys.argv[3] if len(sys.argv) > 3 else "ACTIVE"
    create_user(email, password, status)
