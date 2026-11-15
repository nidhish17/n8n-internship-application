from peewee import SqliteDatabase, Model, IntegerField, CharField, Check, DateField, TextField, BooleanField, chunked
from pathlib import Path


ROOT_DB_DIR = Path(__file__).resolve().parent.parent

DB_PATH = ROOT_DB_DIR / "internships.db"

db = SqliteDatabase(DB_PATH, {
    "foreign_keys": 1,
    "journal_mode": "wal"
})


class BaseModel(Model):
    class Meta:
        database = db

class Internship(BaseModel):

    internship_type_choices = (
        ("free", "Free"),
        ("stipend", "Stipend"),
        ("paid", "Paid")
    )

    work_mode_choices = (
        ("onsite", "Onsite"),
        ("hybrid", "Hybrid"),
        ("online", "Online"),
    )

    internship_id = IntegerField()
    title = CharField(max_length=1000)
    slug = CharField(unique=True)
    internship_type = CharField(choices=internship_type_choices, constraints=[Check("internship_type in ('free', 'stipend', 'paid')")])
    duration = IntegerField(null=True)
    vacancy = IntegerField(null=True)
    total_positions = IntegerField(null=True)
    application_deadline = DateField(null=True)
    description = TextField(null=True)
    workmode = CharField(choices=work_mode_choices, constraints=[Check("workmode in ('onsite', 'online', 'hybrid')")], null=True)
    is_job_offered = BooleanField(default=False)
    job_offered_package = CharField(null=True)
    city = CharField(max_length=255, default="")

    application_link = CharField(max_length=500)
    company_details_page_link = CharField(max_length=500)





with db:
    db.create_tables([Internship], safe=True)
    print("db create successfully")

def insert_internships(internships: list[dict]):
    with db.connection_context():
        with db.atomic():
            for batch in chunked(internships, 100):
                Internship.insert_many(batch).execute()


