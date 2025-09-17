from app import create_app, db
from app.models import User, Incident, Comment, Media

app = create_app()
app.app_context().push()

# Clear existing data
db.drop_all()
db.create_all()

# Users
admin = User(
    name="Admin User",
    email="admin@test.com",
    phone="0700000000",
    role="admin",
    points=100,
)
admin.password = "admin123"

user1 = User(
    name="John Doe",
    email="john@test.com",
    phone="0711111111",
    points=50,
)
user1.password = "password"

user2 = User(
    name="Jane Doe",
    email="jane@test.com",
    phone="0722222222",
    points=75,
)
user2.password = "password"

db.session.add_all([admin, user1, user2])
db.session.commit()

# Incidents
incident1 = Incident(
    title="Broken Streetlight",
    description="Streetlight not working",
    latitude=1.2921,
    longitude=36.8219,
    status="investigating",
    created_by=user1.id,
)

incident2 = Incident(
    title="Pothole",
    description="Large pothole on road",
    latitude=1.2950,
    longitude=36.8220,
    status="resolved",
    created_by=user2.id,
)

db.session.add_all([incident1, incident2])
db.session.commit()

# Comments
comment1 = Comment(
    text="Please fix soon",
    incident_id=incident1.id,
    created_by=user2.id,
)

comment2 = Comment(
    text="Temporary fix applied",
    incident_id=incident2.id,
    created_by=admin.id,
)

db.session.add_all([comment1, comment2])
db.session.commit()

# Media
media1 = Media(
    filename="streetlight.jpg",
    file_url="/uploads/streetlight.jpg",
    incident_id=incident1.id,
    uploaded_by=user1.id,
)

media2 = Media(
    filename="pothole.jpg",
    file_url="/uploads/pothole.jpg",
    incident_id=incident2.id,
    uploaded_by=user2.id,
)

db.session.add_all([media1, media2])
db.session.commit()

# ✅ Print results with timestamps
print("\n✅ Database seeded successfully!\n")
print("Users:")
for u in User.query.all():
    print(f"- {u.name} ({u.email}) role={u.role}, created_at={u.created_at}, updated_at={u.updated_at}")

print("\nIncidents:")
for i in Incident.query.all():
    print(f"- {i.title}: status={i.status}, created_by={i.created_by}, created_at={i.created_at}")

print("\nComments:")
for c in Comment.query.all():
    print(f"- {c.text} (incident_id={c.incident_id}, by user={c.created_by}, created_at={c.created_at})")

print("\nMedia:")
for m in Media.query.all():
    print(f"- {m.filename} -> {m.file_url} (incident_id={m.incident_id}, by user={m.uploaded_by}, created_at={m.created_at})")


# # seed.py
# from app import create_app, db
# from app.models import User, Incident, Comment, Media

# app = create_app()
# app.app_context().push()

# # Clear existing data
# db.drop_all()
# db.create_all()

# # ==========================
# # Users
# # ==========================
# admin = User(
#     name="Admin User",
#     email="admin@test.com",
#     phone="0700000000",
#     role="admin",
#     points=100
# )
# admin.password = "admin123"

# user1 = User(
#     name="John Doe",
#     email="john@test.com",
#     phone="0711111111",
#     points=50
# )
# user1.password = "password"

# user2 = User(
#     name="Jane Doe",
#     email="jane@test.com",
#     phone="0722222222",
#     points=75
# )
# user2.password = "password"

# db.session.add_all([admin, user1, user2])
# db.session.commit()

# # ==========================
# # Incidents
# # ==========================
# incident1 = Incident(
#     title="Broken Streetlight",
#     description="Streetlight not working",
#     latitude=1.2921,
#     longitude=36.8219,
#     status="investigating",
#     created_by=user1.id
# )

# incident2 = Incident(
#     title="Pothole",
#     description="Large pothole on road",
#     latitude=1.2950,
#     longitude=36.8220,
#     status="resolved",
#     created_by=user2.id
# )

# db.session.add_all([incident1, incident2])
# db.session.commit()

# # ==========================
# # Comments
# # ==========================
# comment1 = Comment(
#     text="Please fix soon",
#     incident_id=incident1.id,
#     created_by=user2.id
# )

# comment2 = Comment(
#     text="Temporary fix applied",
#     incident_id=incident2.id,
#     created_by=admin.id
# )

# db.session.add_all([comment1, comment2])
# db.session.commit()

# # ==========================
# # Media
# # ==========================
# media1 = Media(
#     filename="streetlight.jpg",
#     file_url="/uploads/streetlight.jpg",
#     incident_id=incident1.id,
#     uploaded_by=user1.id
# )

# media2 = Media(
#     filename="pothole.jpg",
#     file_url="/uploads/pothole.jpg",
#     incident_id=incident2.id,
#     uploaded_by=user2.id
# )

# db.session.add_all([media1, media2])
# db.session.commit()

# print("✅ Database seeded successfully!")
