import pandas as pd
import os
from io import StringIO
from datetime import datetime
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import clickhouse_connect

# SharePoint URL and credentials
sharepoint_base_url = ''
sharepoint_user = ''
sharepoint_password = ''


# Authenticate to SharePoint
auth = AuthenticationContext(sharepoint_base_url)
auth.acquire_token_for_user(sharepoint_user, sharepoint_password)
ctx = ClientContext(sharepoint_base_url, auth)
web = ctx.web
ctx.load(web)
ctx.execute_query()
print('Connected to SharePoint:', web.properties['Title'])
