# Database so we can keep script size low
db_url = "postgresql://username:password@host_address/db_name"

# Used to secure the web panel.
secret_key = "please_change_thank_you"

# Sentry configuration for error logging.
use_sentry = False
sentry_dsn = "https://public@sentry.example.com/1"

# EULA text, presented upon first launch of channel.
# You may wish to change this to read from a file.
eula_text = "Default terms and conditions."
