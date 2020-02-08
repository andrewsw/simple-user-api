from users import create_app
from werkzeug.serving import run_simple


def main():
    run_simple(
        'localhost',
        5000,
        create_app(),
        use_reloader=True,
    )


main()
