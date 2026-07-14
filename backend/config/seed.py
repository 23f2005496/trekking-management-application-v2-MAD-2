from app import db
from datetime import date
from app.models.staff import Staff
from app.models.trek import Trek
from app.models.user import User

# Sample data
users_data = [
    {
        "email": "vikas123@gmail.com",
        "password": "password",
        "full_name": "Vikas Sharma",
        "contact": "7945449525",
        "role": 'trekker'
    },
    {
        "email": "rahul134@gmail.com",
        "password": "password",
        "full_name": "Rahul Singh",
        "contact": "9658469525",
        "role": 'trekker'
    },
    {
        "email": "harshit235@gmail.com",
        "password": "password",
        "full_name": "Harshit Paliwal",
        "contact": "9956459565",
        "role": 'trekker'
    },
    {
        "email": "alex@staff.com",
        "password": "password",
        "full_name": "Alex Wick",
        "contact": "7976894534",
        "role": 'staff'
    },
    {
        "email": "bob@staff.com",
        "password": "password",
        "full_name": "Bob Smith",
        "contact": "7857584335",
        "role": 'staff'
    },
    {
        "email": "john@staff.com",
        "password": "password",
        "full_name": "John Doe",
        "contact": "9855284656",
        "role": 'staff'
    },
    {
        "email": "brook@staff.com",
        "password": "password",
        "full_name": "Brook Swan",
        "contact": "7976894534",
        "role": 'staff'
    },
]

staffs_data = [
            {
                "email": "alex@staff.com",
                "password": "password",
                "full_name": "Alex Wick",
                "contact": "7976894534",
                "role": 'staff'
            },
            
            {
                "email": "bob@staff.com",
                "password": "password",
                "full_name": "Bob Smith",
                "contact": "7857584335",
                "role": 'staff'
            },

            {
                "email": "john@staff.com",
                "password": "password",
                "full_name": "John Doe",
                "contact": "9855284656",
                "role": 'staff'
            },

            {
                "email": "brook@staff.com",
                "password": "password",
                "full_name": "Brook Swan",
                "contact": "9685285846",
                "role": 'staff'
            },

    ]

treks_data = [
            {
                "name": "Kedarkantha Trek",
                "location": "Uttarakhand",
                "difficulty": "Easy",
                "duration": "5 Days",
                "slots": 150,
                "start_date": date(2026, 7, 20),
                "end_date": date(2026, 7, 25),
                "image": "kedarkantha_trek.jpg"
             },

            {
                "name": "Tungnath Trek",
                "location": "Uttarakhand",
                "difficulty": "Easy",
                "duration": "4 Days",
                "slots": 100,
                "start_date": date(2026, 7, 30),
                "end_date": date(2026, 8, 3),
                "image": "tungnath_trek.jpg"
             },

            {
                "name": "Har Ki Dun Trek",
                "location": "Uttarakhand",
                "difficulty": "Moderate",
                "duration": "7 Days",
                "slots": 50,
                "start_date": date(2026, 8, 9),
                "end_date": date(2026, 8, 16),
                "image": "har_ki_dun_trek.jpg"
             },

            {
                "name": "Hampta Pass Trek",
                "location": "Himachal Pradesh",
                "difficulty": "Moderate",
                "duration": "6 Days",
                "slots": 70,
                "start_date": date(2026, 8, 21),
                "end_date": date(2026, 8, 27),
                "image": "hampta_pass_trek.jpg"
             },

            {
                "name": "Goechala Trek",
                "location": "Sikkim",
                "difficulty": "Hard",
                "duration": "10 Days",
                "slots": 20,
                "start_date": date(2026, 9, 2),
                "end_date": date(2026, 9, 12),
                "image": "goechala_trek.jpg"
             },

            {
                "name": "Everest Base Camp Trek",
                "location": "Nepal",
                "difficulty": "Hard",
                "duration": "13 Days",
                "slots": 15,
                "start_date": date(2026, 9, 18),
                "end_date": date(2026, 9, 30),
                "image": "everest_base_camp_trek.jpg"
             },
]


def seed_database():
    # Add users
    for user_data in users_data:
        user = User(
            email=user_data["email"],
            full_name=user_data["full_name"],
            contact=user_data["contact"],
            role=user_data["role"]
        )
        user.set_password(user_data["password"])
        db.session.add(user)
        db.session.commit()

    
    # Add staff
    for staff_data in staffs_data:
        user = User.query.filter_by(email=staff_data["email"]).first()
        
        staff = Staff(
            email=staff_data["email"],
            full_name=staff_data["full_name"],
            contact=staff_data["contact"],
            user_id=user.id
        )
        db.session.add(staff)
        db.session.commit()


    # Add treks
    for trek_data in treks_data:
        trek = Trek(
                name=trek_data["name"],
                location=trek_data["location"],
                difficulty=trek_data["difficulty"],
                duration=trek_data["duration"],
                slots=trek_data["slots"],
                start_date=trek_data["start_date"],
                end_date=trek_data["end_date"],
                image=trek_data["image"]
        )
        db.session.add(trek)
        db.session.commit()

