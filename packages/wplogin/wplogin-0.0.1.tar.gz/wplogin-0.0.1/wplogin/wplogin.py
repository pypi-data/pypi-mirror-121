# __wplogin__.py
# import wplogin
# By GreenWorld Dev
import requests

wp_login = wpurl + '/wp-login.php'
wp_admin = wpurl + '/wp-admin/'
username = user
password = pw

with requests.Session() as s:
    headers1 = {'Cookie':'wordpress_test_cookie=WP Cookie check' }
    datas={
        'log':username, 'pwd':password, 'wp-submit':'Log In',
        'redirect_to':wp_admin, 'testcookie':'1'
    }
    s.post(wp_login, headers=headers1, data=datas)
    resp = s.get(wp_admin)
    print(resp.text)