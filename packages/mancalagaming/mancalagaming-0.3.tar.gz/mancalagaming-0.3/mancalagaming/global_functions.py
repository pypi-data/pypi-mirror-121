import json
import random
import string
import requests

chars = '+-*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
chars_username = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
chars_phone_number = '1234567890'
symbols = string.ascii_letters + string.digits + string.punctuation
domains_list = ['tut.by', 'yandex.com', 'google.com']
EMAIL_DOMAINS = (
    '@gmail.com',
    '@yandex.com',
    '@yahoo.com',
    '@live.com',
    '@outlook.com',
    '@protonmail.com',
)

CALLING_CODES = [
    '+1', '+7', '+20', '+27', '+30', '+31', '+32', '+33', '+34', '+36', '+39', '+40', '+41', '+43', '+44', '+44',
    '+44', '+44', '+45', '+46', '+47', '+48', '+49', '+51', '+52', '+53', '+54', '+55', '+56', '+56', '+57', '+58',
    '+60', '+61', '+61', '+61', '+62', '+63', '+64', '+64', '+64', '+65', '+66', '+77', '+81', '+82', '+84', '+86',
    '+90', '+91', '+92', '+93', '+94', '+95', '+98', '+211', '+212', '+213', '+216', '+218', '+220', '+221', '+222',
    '+223', '+224', '+225', '+226', '+227', '+228', '+229', '+230', '+231', '+232', '+233', '+234', '+235', '+236',
    '+237', '+238', '+239', '+240', '+241', '+242', '+243', '+244', '+245', '+246', '+246', '+247', '+248', '+249',
    '+250', '+251', '+252', '+253', '+254', '+255', '+255', '+256', '+257', '+258', '+260', '+261', '+262', '+262',
    '+263', '+264', '+265', '+266', '+267', '+268', '+269', '+290', '+291', '+297', '+298', '+299', '+350', '+351',
    '+352', '+353', '+354', '+355', '+356', '+357', '+358', '+359', '+370', '+371', '+372', '+373', '+374', '+375',
    '+376', '+377', '+378', '+379', '+380', '+381', '+382', '+383', '+385', '+386', '+387', '+389', '+420', '+421',
    '+423', '+500', '+500', '+501', '+502', '+503', '+504', '+505', '+506', '+507', '+508', '+509', '+590', '+590',
    '+590', '+591', '+592', '+593', '+594', '+595', '+596', '+596', '+597', '+598', '+670', '+672', '+672', '+673',
    '+674', '+675', '+676', '+677', '+678', '+679', '+680', '+681', '+682', '+683', '+685', '+686', '+687', '+688',
    '+689', '+690', '+691', '+692', '+800', '+808', '+850', '+852', '+853', '+855', '+856', '+870', '+878', '+880',
    '+881', '+886', '+960', '+961', '+962', '+963', '+964', '+965', '+966', '+967', '+968', '+970', '+971', '+972',
    '+973', '+974', '+975', '+976', '+977', '+992', '+993', '+994', '+995', '+996', '+998', '+1242', '+1246',
    '+1264', '+1268', '+1268', '+1284', '+1340', '+1345', '+1441', '+1473', '+1649', '+1664', '+1670', '+1671',
    '+1684', '+1721', '+1758', '+1767', '+1784', '+1808', '+1808', '+1849', '+1868', '+1869', '+1869', '+1876',
    '+1939', '+2908', '+4779', '+4779', '+5399', '+5993', '+5994', '+5997', '+5997', '+5999', '+8810', '+8813',
    '+8817', '+8818', '+35818', '+88213', '+88216', '+90392', '+99534', '+99544',
]

def generate_password(length):
    import string
    from secrets import choice

    alphabet = string.ascii_letters + string.digits  # + string.punctuation
    while True:
        password = ''.join(choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password

def generate_secure_password(length):
    import random
    secure_random = random.SystemRandom()
    password = "".join(secure_random.choice(symbols) for i in range(length))
    return password

def user_password(number, length):
    import random
    for n in range(number):
        password = ''
        for i in range(length):
            password += random.choice(chars)
        return password

def user_phone(number, length):
    import random
    for n in range(number):
        phone_number = ''
        for i in range(length):
            phone_number += random.choice(chars_phone_number)
        return phone_number

def user_email():
    """Generate a random email.

    :param domains: List of custom domains for emails.
    :type domains: list or tuple
    :return: Email address.

    :Example:
        foretime10@live.com
    """
    import random
    domains = EMAIL_DOMAINS
    domain = random.choice(domains)
    if not domain.startswith('@'):
        domain = '@{}'.format(domain)
    name = "".join(random.SystemRandom().choice(chars_username) for i in range(8))
    return '{name}{domain}'.format(
        name=name,
        domain=domain,
    )

def write_data_to_json_file(f, target_data):
    """
    : Функция записывает массив target_data в файл 'f' в формате JSON
    :output example : 'test 12-03-2021 14-57-37.json'
    :param f: test
    :param target_data: json.dumps(getAsyncResponse, indent=2)
    :example: write_data_to_json_file('test', getAsyncResponse)
    :www source: https://stackoverflow.com/questions/9170288/pretty-print-json-data-to-a-file-using-python
    """
    import datetime
    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
    file = open(f + ' {}.json'.format(dt), 'a')  # открываем куда писать полученные данные
    file.write(json.dumps(target_data, indent=2))  # записываем файл
    file.close()  # закрываем файл


def print2file(f, target_data):
    import datetime
    # dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y"))
    file = open(f + ' {}.json'.format(dt), 'a')  # открываем куда писать полученные данные
    file.write(target_data)  # записываем файл
    file.write('\n')
    file.close()  # закрываем файл


def write_data_to_disk(f, target_data: list):
    import datetime
    """  Функция записывает массив target_data в файл
    """
    dt = '{}'.format(datetime.datetime.today().strftime("%d-%m-%Y %H-%M-%S"))
    file = open(f, 'a')  # открываем куда писать полученные данные
    file.write("\n".join(target_data))  # записываем файл
    file.close()  # закрываем файл

def read_data_from_disk():
    pass

def findall(v, k):
    """
    : рекурсивный поиск - найти конкретное значение JSON по ключу
    :param v: где ищем
    :param k: что ищем
    :return: results = findall(data, "WinStateInfo")
    with open('c:/testing/response2.json') as json_file:
        data = json.load(json_file)
        data_str = json.dumps(data)
    """
    if type(v) == type({}):
        for k1 in v:
            if k1 == k:
                print(v[k1])
                return v[k1]
            result = findall(v[k1], k)
            if result is not None:
                return result

    if type(v) == type([]):
        for k1 in v:
            result = findall(k1, k)
            if result is not None:
                return result

class Reddy:
    def __init__(self, toReddy=False, gameLine=''):
        self.toReddy = toReddy
        self.gameLine = gameLine
        self.token_bot = 'BGCcKgM79OMwRAJe-hWkZwpsRaIJ0-xx'
        self.id_bot = 72220000235

        if self.gameLine == 'xSpin':
            self.reddy_id_chat = 331716
        if self.gameLine == 'xPlay':
            self.reddy_id_chat = 331717
        if self.gameLine == 'xGame':
            self.reddy_id_chat = 331721
        if self.gameLine == 'xCard':
            self.reddy_id_chat = 331722
        if self.gameLine == 'xLine':
            self.reddy_id_chat = 331723
        if self.gameLine == 'mm3':
            self.reddy_id_chat = 331707
        if self.gameLine == 'mm4':
            self.reddy_id_chat = 331704
        if self.gameLine == 'mm5':
            self.reddy_id_chat = 324537
        if self.gameLine == 'mm6':
            self.reddy_id_chat = 323826
        if self.gameLine == 'mm7':
            self.reddy_id_chat = 324386
        if self.gameLine == 'mm8':
            self.reddy_id_chat = 331709
        if self.gameLine == 'mm9':
            self.reddy_id_chat = 331710
        if self.gameLine == 'mm10':
            self.reddy_id_chat = 331711
        if self.gameLine == 'mm11':
            self.reddy_id_chat = 333071
        else:
            pass

        return

    def send_message2reddy(self, *args):
        aa = []
        for v in args:
            aa.append(str(v))
        if self.toReddy:
            for a in range(len(aa)):
                url = F"https://bot.reddy.team/bot{self.token_bot}/send?chat={self.reddy_id_chat}&msg={aa[a]}"
                response = requests.get(url)
                print(f'Было отправлено сообщение в Reddy. HTTP: {response}')
            else:
                pass

class RTP:
    def __init__(self, userCount=0, currentRTP=0):
        self.userCount = userCount
        self.currentRTP = currentRTP
        self.start_users_rtp_90 = 190000  # 90%
        self.start_users_rtp_95 = 195000  # 95%
        self.start_users_rtp_96 = 196000  # 96%
        self.start_users_rtp_97 = 197000  # 97%
        self.start_users_rtp_120 = 120000  # 120%

        if self.currentRTP == 90:
            self.start_users_rtp = self.start_users_rtp_90
        if self.currentRTP == 95:
            self.start_users_rtp = self.start_users_rtp_95
        if self.currentRTP == 96:
            self.start_users_rtp = self.start_users_rtp_96
        if self.currentRTP == 97:
            self.start_users_rtp = self.start_users_rtp_97
        if self.currentRTP == 120:
            self.start_users_rtp = self.start_users_rtp_120
        else:
            self.start_users_rtp = self.start_users_rtp_90

        return

    def setRTP(self):
        rtp_user_count = self.userCount
        rtp_user_range = range(self.start_users_rtp, self.start_users_rtp + rtp_user_count)
        rtp_user_list = []

        for xxx in range(len(rtp_user_range)):
            rtp_user_list.append(rtp_user_range[xxx])

        return rtp_user_count, rtp_user_range, rtp_user_list


class Logger(object):

    def __init__(self, fileName='', toFile=False, toConsole=False):
        self.fileName = fileName
        self.toFile = toFile
        self.toConsole = toConsole
        return

    def printml(self, *args):
        aa = []
        toprint = ''
        for v in args:
            aa.append(str(v))
            toprint = toprint + str(v) + ' '
        if self.toFile and self.toConsole:
            f = open(self.fileName, 'a')
            for a in range(len(aa)):
                f.write(aa[a])
                f.write('\n')
                print(aa[a])
                # print('\n')
            f.close()
        elif self.toFile:
            f = open(self.fileName, 'a')
            for a in range(len(aa)):
                f.write(aa[a])
                f.write('\n')
            f.close()
        elif self.toConsole:
            for a in range(len(aa)):
                print(aa[a])
        else:
            pass
        return
