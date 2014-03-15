port = 8765
host = '127.0.0.1'

handler_path = 'handler.' # For import: separated and ended by dot "." char
routes = [
    # URL regex pattern, module, handler class 
    (r'/(.*)', 'page', 'View'),
]
env = dict(
    common=dict(
        template_path='tmpl/',
        cookie_secret='',
        xsrf_cookies=True,
        login_url='',
    ),
    local=dict(
        debug=True,
        compiled_template_cache=False,
        google_consumer_key='',
        google_consumer_secret='',
        facebook_api_key='',
        facebook_secret='',
    )
)