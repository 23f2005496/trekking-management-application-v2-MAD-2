import os
from app import db
from app.models.user import User
from config.seed import seed_database
from flask_migrate import upgrade, migrate


def create_admin():
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_full_name = os.getenv("ADMIN_FULL_NAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    admin = User.query.filter_by(role="admin").first()

    if not admin:
        admin = User(
            email=admin_email,
            full_name=admin_full_name,
            role="admin"
        )
        admin.set_password(admin_password)

        db.session.add(admin)
        db.session.commit()

        print("✅ Admin created successfully!")
    else:
        print("⚠️ Admin already exists!")


def register_commands(app):

    # 🔹 Create DB (using migrations)
    @app.cli.command("create-db")
    def create_db():
        """Apply migrations and create admin user"""
        migrate(message="auto migration for create-db!")
        upgrade()
        create_admin()
        print("✅ Database setup completed using migrations!")

    # 🔹 Seed Data
    @app.cli.command("seed-db")
    def seed_db():
        """Seed database with initial data"""
        seed_database()
        print("✅ Database seeded successfully!")

    # 🔹 Reset DB (VERY useful)
    @app.cli.command("reset-db")
    def reset_db():
        """Drop and recreate database"""
        confirm = input("⚠️ This will DELETE all data. Continue? (y/n): ")

        if confirm.lower() == "y":
            db.drop_all()

            migrate(message="auto migration for reset-db!")
            upgrade()

            create_admin()
            print("🔥 Database reset completed using migrations!")
        else:
            print("❌ Operation cancelled.")