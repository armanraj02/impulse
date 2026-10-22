import os
print(f'SMTP_DRY_RUN={os.environ.get("SMTP_DRY_RUN")}')
print(f'SMTP_HOST={os.environ.get("SMTP_HOST")}')
print(f'SMTP_PORT={os.environ.get("SMTP_PORT")}')
print(f'SMTP_USERNAME={os.environ.get("SMTP_USERNAME")}')
print(f'SMTP_FROM={os.environ.get("SMTP_FROM")}')
print(f'SMTP_TO={os.environ.get("SMTP_TO")}')
print(f'SMTP_USE_TLS={os.environ.get("SMTP_USE_TLS")}')
password = os.environ.get('SMTP_PASSWORD')
if password and len(password) > 0:
    print('SMTP_PASSWORD is SET (Hidden)')
else:
    print('SMTP_PASSWORD is EMPTY')
