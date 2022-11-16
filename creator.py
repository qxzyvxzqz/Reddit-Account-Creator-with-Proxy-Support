import requests
from random import choice
from string import ascii_letters
from userAgentRandomizer import userAgents


def captcha():
    return #Add your own code


def proxy():
    proxy_list = []
    with open('proxy.txt', 'r') as f:
        for line in f:
            proxy_list.append(line)
    proxy_value = choice(proxy_list)
    return {'http': f'http://{proxy_value}'.replace('\n', ''), 'https': f'http://{proxy_value}'.replace('\n', '')}


def generate_username():
    res = requests.get('https://www.reddit.com/api/v1/generate_username.json', headers={'user-agent': str(userAgents().random())}, proxies=proxy()).json()
    username = res['usernames'][0]
    return username


def creator():
    try:
        session = requests.session()
        user = generate_username()
        email = ''.join(choice(ascii_letters) for _ in range(0, 16))
        randomVar = "".join([choice(ascii_letters) for _ in range(14)])
        captcha_response = captcha()
        cookie_dict = session.get("https://old.reddit.com/register", headers={"user-agent": str(userAgents().random())}, proxies=proxy()).cookies.get_dict()
        payload = f"op=reg&dest=https%3A%2F%2Fold.reddit.com%2F&user={user}&passwd={randomVar}&passwd2={randomVar}&email={email}%hotmail.com&g-recaptcha-response={captcha_response}&api_type=json"
        response = session.post(f"https://old.reddit.com/register/{user}", data=payload, headers={"user-agent": str(userAgents().random())}, cookies=cookie_dict, proxies=proxy())
        if not response.json()['json']['errors']:
            print(f"[+] {user}:{randomVar}:{email}@hotmail.com")
        else:
            print(f"[-] {response.json()['json']['errors']}")
    except requests.exceptions.ProxyError:
        print("[-] Proxy Disconnected.")


def main():
    count = input("[?] How many accounts do you want to create: ")
    for i in range(int(count)):
        creator()


if __name__ == "__main__":
    main()
