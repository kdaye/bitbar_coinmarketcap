#!/Users/leewi9/.local/share/virtualenvs/leewi9-lzQu0maA/bin/python
# coding=utf-8
"""
# <bitbar.title>coinmarketcap ticker (CNY)</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>leewi9</bitbar.author>
# <bitbar.author.github>leewi9</bitbar.author.github>
# <bitbar.desc>
#   Displays crypto from coinmarketcap
# </bitbar.desc>
# <bitbar.image>http://7xj3js.com1.z0.glb.clouddn.com/Jietu20171026-132926.jpg</bitbar.image>
"""

import time
import requests
from decimal import Decimal

COINS = [
    {'id': 'bitcoin'},
    {'id': 'bitcoin-cash'},
    {'id': 'bitcoin-gold'},
    {'id': 'ethereum'},
    {'id': 'litecoin'},

    {'id': '-'},

    {'id': 'neo'},
    {'id': 'gas'},
    {'id': 'red-pulse'},

    {'id': '-'},
    {'id': 'aeron'},

    {'id': '-'},

    {'id': 'ripple'},
    {'id': 'kucoin-shares'},
    {'id': 'eos'},

    {'id': '-'},

    # {'id': 'ardor'},
    # {'id': 'smartcash'},
    {'id': 'monero'},
    {'id': 'zcash'},
    {'id': 'vertcoin'},
    {'id': 'groestlcoin'},
]

SYMBOLS = {
    'up': '',
    'down': '',
}


def getResult(url):
    #
    retry = 1
    while True:
        if retry == 5:
            print('已重试5次。')
            print('---')
            print('Refresh | refresh=true')
            return ''
        try:
            # print ('try次数：' + str(retry))
            # print ('开始发送请求' + url)
            r = requests.get(url, timeout=3)
            results = r.json()
            # print (r.status_code)
            if r.status_code == requests.codes.ok:
                break
        except requests.exceptions.RequestException as e:
            # print (e)
            retry = retry + 1
            time.sleep(10)
    return results


def main():
    print('[CMC]')
    print('---')

    #
    url = "https://api.coinmarketcap.com/v1/ticker/?convert=CNY"
    #
    results = getResult(url)
    if results == '':
        return

    #
    for coin in COINS:

        #
        coin_id = coin['id']

        #
        if coin_id == '-':
            print('---')
            continue

        #
        flag = 0
        for r in results:
            if coin_id.upper() == r['id'].upper():
                result = r
                flag = 1
                break

        if flag == 0:  # 说明在之前的api返回中没有找到该值，需要单独发送请求
            re = getResult("https://api.coinmarketcap.com/v1/ticker/" + coin_id + "/?convert=CNY")
            if re != '':
                result = re[0]

        value_f = Decimal(float(result['price_cny'])).quantize(Decimal("0.00"))
        value = format(value_f, ',')

        if result['percent_change_24h'] != None:
            change_f = round(float(result['percent_change_24h']), 2)
            change = format(change_f, ',')
        else:
            change_f = 0
            change = ''

        volumn_f = long(float(result['24h_volume_cny']))
        volumn = format(volumn_f, ',')

        if result['total_supply'] != None:
            supply_f = long(float(result['total_supply']))
            supply = format(supply_f, ',')
        else:
            supply = ''

        if result['market_cap_cny'] != None:
            cap_f = long(float(result['market_cap_cny']))
            cap = format(cap_f, ',')
        else:
            cap = ''

        #
        if change_f >= 0:
            color = 'color=#228B22'
        else:
            color = 'color=#8B0000'

        #
        output = ''.join((
            '{:6s}',
            '{:>10s} ',
            ' [{:>7s}] ',
            '{:>15s}',
            '  sup:{:>16s}',
            '  cap:{:>17s}',
            ' | size=14 font=Courier ',
            color
        ))
        print output.format(result['symbol'], value, change, volumn, supply, cap)

    print('---')

    print('Refresh | refresh=true')


if __name__ == "__main__":
    main()
