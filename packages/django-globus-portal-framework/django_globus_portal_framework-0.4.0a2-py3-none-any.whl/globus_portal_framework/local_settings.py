from globus_portal_framework import settings

settings.LOGGING['handlers']['stream']['level'] = 'DEBUG'

DEBUG = True
ALLOWED_HOSTS = ['*']

SECRET_KEY = '70515cd2089caee62f5af9bfec669c0c4c3af4521a5fb5185b96ebb02d8e46d'

# Regular, general local testing keys
SOCIAL_AUTH_GLOBUS_KEY = 'a9efbf1c-08e8-48f6-b48e-4a66e0a6d9fb'
SOCIAL_AUTH_GLOBUS_SECRET = 'NIgGl2LSMW7nZ3Mbwm3MmERM+QLrmefAPlLC+bIIMMI='

# ALCF stuff
# ecb27add-7b02-43a1-9da5-71fb4246395d@clients.auth.globus.org
# SOCIAL_AUTH_GLOBUS_KEY = 'ecb27add-7b02-43a1-9da5-71fb4246395d'
# SOCIAL_AUTH_GLOBUS_SECRET = 'iKaQGZzOj6EhYBOiuXhynRnbBhe7/4sLa03mRrn88GE='

# Globus Preview
# SOCIAL_AUTH_GLOBUS_KEY = '3e99b274-80be-41de-905d-f10853fa454b'
# SOCIAL_AUTH_GLOBUS_SECRET = 'NZpcp0BLWrO6ABagUvKHs6OYy3K1xIOt9kkK6e0JdSw='

# settings.LOGGING['handlers']['stream']['level'] = 'DEBUG'
# settings.LOGGING['loggers']['globus_portal_framework']['level'] = 'DEBUG'


# CONFIDENTIAL_CLIENT_SECRETS = [
#     {'name': 'My Secondary Globus Proxy App',
#      'client_id': '899dde29-6618-490b-8062-e6eb6dea4206',
#      'client_secret': 'lfdMpRU5YmKrCYV1YOn5O1zApLQFiu6hVjWmCf/CCM4='},
# ]

# SOCIAL_AUTH_GLOBUS_SESSIONS = True

# Set to a UUID of a Globus group if you want to restrict access to the portal
# to members of the Globus group.
# Required: The view_my_groups_and_memberships scope above
# Recommended: Add to MIDDLEWARE the following:
#     'globus_portal_framework.middleware.GlobusAuthExceptionMiddleware'
#     This redirects the user for expected exceptions, you need to handle these
#     exceptions yourself if you don't add this.
# SOCIAL_AUTH_GLOBUS_ALLOWED_GROUPS = [
#     {
#         'name': 'Portal Users Group',
#         'uuid': 'f63def4d-b472-11e9-af05-0a075bc69d14'
#     }
# ]

# Preview
# SOCIAL_AUTH_GLOBUS_ALLOWED_GROUPS = [
#     {
#         'name': 'Preview Portal Users Group',
#         'uuid': '05cf14cc-1a81-11e9-846f-0e8ffb13a142'
#     }
# ]
