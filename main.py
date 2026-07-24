import os
import subprocess
import sys


def run_migrations():
    """
    Применяет миграции перед стартом сервера.
    --run-syncdb на случай, если какие-то таблицы без миграций (обычно не нужно
    в этом проекте, но безопасно оставить как подстраховку).
    """
    subprocess.run(
        [sys.executable, 'manage.py', 'migrate', '--run-syncdb'],
        check=True,
    )


def collect_static():
    """
    Собирает статику в STATIC_ROOT. Нужен, только если вы включите
    STATIC_ROOT и будете отдавать статику через collectstatic
    (см. примечание в settings.py ниже) — если используете runserver
    с DEBUG=True, статика отдаётся напрямую из приложений и этот шаг
    можно пропустить.
    """
    subprocess.run(
        [sys.executable, 'manage.py', 'collectstatic', '--noinput'],
        check=False,  # не критично, если STATIC_ROOT не настроен
    )


def run_server():
    port = os.environ.get('PORT', '8000')
    subprocess.run(
        [sys.executable, 'manage.py', 'runserver', f'0.0.0.0:{port}'],
        check=True,
    )


if __name__ == '__main__':
    run_migrations()
    run_server()