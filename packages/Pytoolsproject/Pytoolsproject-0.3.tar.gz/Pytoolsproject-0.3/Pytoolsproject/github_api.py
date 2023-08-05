import requests


def buscar_avatar(usuario):

    """
    Busca o avatar de um usuário no Github.

    :param usuário: str com o nome de usuário no github.
    :return: str com o link do avatar
    """
    url = f' https://api.github.com/users/{usuario}'
    response = requests.get(url)
    return response.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('tiago1figueira'))
