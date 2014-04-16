import os
import os.path

path = os.path.dirname(__file__)
host = '127.0.0.1'
port = 7654

timezone = 'Asia/Tokyo'
setting = dict(
    template_path='tmpl/',
    cookie_secret='FILL_YOURS_HERE',
    xsrf_cookies=True,
    login_url='',
)
routes = [
    # URL ("pattern", "module.Handler")
]

# Local
debug = True

# Deploy