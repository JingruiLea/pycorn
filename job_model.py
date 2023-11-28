from mongoengine import Document, StringField, DateTimeField


class Job(Document):
    job_id = StringField(required=True)
    url = StringField(required=True)
    cron_expression = StringField()
    run_at = DateTimeField()
