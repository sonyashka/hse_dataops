import os
from pathlib import Path

c = get_config()

c.JupyterHub.bind_url = f"http://0.0.0.0:{os.environ.get('JUPYTERHUB_PORT', '8000')}"

c.ConfigurableHTTPProxy.api_url = "http://127.0.0.1:8001"
c.ConfigurableHTTPProxy.should_start = True
c.ConfigurableHTTPProxy.auth_token = os.environ.get('JUPYTERHUB_PROXY_AUTH_TOKEN', 'default-proxy-token')

db_url = os.environ.get(
    'JUPYTERHUB_DB_URL',
    f"postgresql://{os.environ.get('POSTGRES_USER', 'jupyterhub')}:"
    f"{os.environ.get('POSTGRES_PASSWORD', 'jupyterhub')}@"
    f"{os.environ.get('POSTGRES_HOST', 'postgres')}:"
    f"{os.environ.get('POSTGRES_PORT', '5432')}/"
    f"{os.environ.get('POSTGRES_DB', 'jupyterhub')}"
)
c.JupyterHub.db_url = db_url

c.JupyterHub.data_dir = '/srv/jupyterhub/data'
c.JupyterHub.log_dir = '/srv/jupyterhub/log'
c.JupyterHub.cookie_secret_file = f"{c.JupyterHub.data_dir}/jupyterhub_cookie_secret"
c.JupyterHub.proxy_auth_token = os.environ.get('JUPYTERHUB_PROXY_AUTH_TOKEN', '')

c.JupyterHub.cookie_secret = os.environ.get('JUPYTERHUB_COOKIE_SECRET', '').encode('utf-8')
c.JupyterHub.last_activity_interval = 300

c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'

c.Authenticator.admin_users = {os.environ.get('JUPYTERHUB_ADMIN_USER', 'admin')}
c.Authenticator.allowed_users = set()
c.Authenticator.allow_all = True

c.Authenticator.add_user_cmd = ['adduser', '-q', '--gecos', '""', '--disabled-password', '--force-badname']
c.Authenticator.delete_invalid_users = True

c.JupyterHub.spawner_class = 'jupyterhub.spawner.SimpleLocalProcessSpawner'

c.Spawner.notebook_dir = '~/notebooks'
c.Spawner.default_url = '/lab'
c.Spawner.cpu_limit = 2
c.Spawner.memory_limit = '2G'
c.Spawner.environment = {
    'JUPYTER_ENABLE_LAB': 'yes'
}

c.JupyterHub.shutdown_on_logout = False
c.Spawner.start_timeout = 60
c.Spawner.http_timeout = 60

c.JupyterHub.log_level = 'INFO'
c.JupyterHub.log_datefmt = '%Y-%m-%d %H:%M:%S'
c.JupyterHub.log_format = '[%(levelname)1.1s %(asctime)s.%(msecs).03d %(name)s] %(message)s'

def pre_spawn_hook(spawner):
    """Хук перед запуском пользовательского сервера"""
    username = spawner.user.name
    spawner.log.info(f"Запуск сервера для пользователя: {username}")

c.Spawner.pre_spawn_hook = pre_spawn_hook

print(f"JupyterHub конфигурация загружена. Админ: {c.Authenticator.admin_users}")
print(f"База данных: {c.JupyterHub.db_url}")