import requests
import re

session = requests.Session()
url = "https://coloniaprev-ac815.web.app/auth/login"

print("1. Buscando a pagina de login...")
response = session.get(url)
print("Status GET:", response.status_code)

match = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', response.text)
if match:
    csrf_token = match.group(1)
    print("CSRF Token encontrado:", csrf_token)
else:
    print("CSRF Token não encontrado!")
    csrf_token = ''

data = {
    'email': 'admin@coloniaprev.com.br',
    'senha': '123456',
    'csrf_token': csrf_token,
    'submit': 'Entrar'
}

print("2. Enviando requisição de login...")
post_response = session.post(url, data=data, allow_redirects=False)
print("Status POST:", post_response.status_code)
print("Headers:", post_response.headers)

if post_response.status_code == 302:
    print("Redirecionando para:", post_response.headers.get('Location'))
else:
    print("Ocorreu um erro no login. HTML retornado:")
    print(post_response.text[:500])

print("\nCookies na sessao:")
print(session.cookies.get_dict())
