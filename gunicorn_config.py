# gunicorn_config.py
bind = "0.0.0.0:10000"
workers = 2
timeout = 120  # 2 minutes
graceful_timeout = 30
keepalive = 5