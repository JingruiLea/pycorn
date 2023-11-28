import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    ERROR_404_HELP = False
    dotenv_filename = '.env'
    if os.environ.get("FLASK_ENV") is not None:
        dotenv_filename = f'.env.{os.environ.get("FLASK_ENV")}'

    print(f'load env file: {dotenv_filename}')
    load_dotenv(dotenv_path=os.path.join(basedir, dotenv_filename), override=True)

    # DB
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWD = os.environ.get('DB_PASSWD')
    DB_NAME = os.environ.get('DB_NAME')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
