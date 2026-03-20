import os
import sys
from jupyterhub.auth import PAMAuthenticator
from jupyterhub.spawner import SimpleLocalProcessSpawner

# Настройка аутентификации
c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'
c.PAMAuthenticator.open_sessions = True
c.PAMAuthenticator.service = 'login'

# Настройка spawner
c.JupyterHub.spawner_class = 'jupyterhub.spawner.SimpleLocalProcessSpawner'
c.SimpleLocalProcessSpawner.default_url = '/lab'

# Настройка сети и портов
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8081
c.JupyterHub.port = 8000
c.JupyterHub.ip = '0.0.0.0'

# Настройка путей
c.JupyterHub.db_url = '/home/jupyter/jupyterhub.sqlite'
c.JupyterHub.cookie_secret_file = '/home/jupyter/jupyterhub_cookie_secret'
c.JupyterHub.proxy_auth_token = os.urandom(32).hex()

# Администраторы
admin_users = os.environ.get('JUPYTERHUB_ADMIN_USERS', '').split(',')
if admin_users and admin_users[0]:
    c.Authenticator.admin_users = set(admin_users)

# Разрешенные пользователи
allowed_users = os.environ.get('JUPYTERHUB_ALLOWED_USERS', '').split(',')
if allowed_users and allowed_users[0]:
    c.Authenticator.allowed_users = set(allowed_users)

# Настройка таймаутов
c.JupyterHub.shutdown_on_logout = False
c.JupyterHub.cleanup_servers = True
c.Spawner.start_timeout = 60
c.Spawner.http_timeout = 30

# Настройка ресурсов
c.Spawner.mem_limit = '1G'
c.Spawner.cpu_limit = 1.0

# Настройка JupyterLab
c.Spawner.args = ['--NotebookApp.default_url=/lab']

# Логирование
c.JupyterHub.log_level = 'INFO'
c.JupyterHub.debug = False

# Путь для работы пользователей
c.Spawner.notebook_dir = '/home/jupyter/work'

# Дополнительные настройки безопасности
c.JupyterHub.allow_named_servers = False
c.JupyterHub.authenticate_prometheus = False

print(f"JupyterHub configuration loaded")
print(f"Admin users: {c.Authenticator.admin_users}")
print(f"Allowed users: {c.Authenticator.allowed_users}")