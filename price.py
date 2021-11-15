import requests
from requests.exceptions import HTTPError
#import json
import re

def comma_sep(num):
    if num > 1000:
        pattern = '\B(?=(\d{3})+(?!\d))'
        return re.sub(pattern, ',', str(num))
    return str(num)

def fetch_price_to(url_xwp, url_btc):
    try:
        response_xwp = requests.get(url_xwp, timeout=5)
        response_btc = requests.get(url_btc, timeout=5)
        
        json_xwp = response_xwp.json()
        json_btc =response_btc.json()

        if response_xwp.status_code == 200 and response_btc.status_code == 200:
            # getting data
            initial = float(json_xwp['initialprice'])
            xwp_btc = float(json_xwp['price'])
            high_24 = float(json_xwp['high'])
            low_24 = float(json_xwp['low'])
            volume = float(json_xwp['volume'])
            btc_usd = json_btc['USD']['last']

            h_24 = (xwp_btc-initial)/initial * 100
            if h_24 > 0:
                h_24 = '+%.2f%%'%h_24
            elif h_24 < 0:
                h_24 = '-%.2f%%'%h_24
            msg = '```price    : %.5f $ | %d satoshi \nH|L(usd) : %.5f $ | %.5f $\nH|L(sat) : %d sat   | %d sat\n24h Chg  : %s(₿)\nVol      : %s $   | %.5f ₿```'%(xwp_btc*btc_usd,
                    xwp_btc*100000000,
                    high_24*btc_usd,
                    low_24*btc_usd,
                    high_24*100000000,
                    low_24*100000000,
                    h_24,
                    comma_sep(int(volume*btc_usd)),
                    volume)
            return msg

    except HTTPError as http_err:
        #raise DiscordException 
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        #raise DiscordException
        print(f'Other error occurred: {err}')

def fetch_price_cg(xwp_cg):
    try:
        response_xwp = requests.get(xwp_cg, params={'ids': 'swap',
                                 'vs_currencies': 'usd,btc',
                                 'include_market_cap':'true',
                                 'include_24hr_vol':'true',
                                 'include_24hr_change':'true'}, timeout=5)
        json_xwp = response_xwp.json()

        if response_xwp.status_code == 200:
            # getting data
            xwp_btc = json_xwp['swap']['btc']
            xwp_usd = json_xwp['swap']['usd']
            volume = json_xwp['swap']['usd_24h_vol']
            h_24 = json_xwp['swap']['usd_24h_change']
            mc_btc = json_xwp['swap']['btc_market_cap']
            mc_usd = json_xwp['swap']['usd_market_cap']

            if h_24 > 0:
                h_24 = '+%.2f%%'%h_24
            elif h_24 < 0:
                h_24 = '-%.2f%%'%h_24
            
            msg = '```price     : %.5f $ | %d satoshi\n24h Chg   : %s($)\nVol       : %s $\nMarket Cap: %s $ | %.5f ₿```'%(xwp_usd,
                    int(xwp_btc*100000000),
                    h_24,
                    comma_sep(int(volume)),
                    comma_sep(int(mc_usd)),
                    mc_btc)
            return msg

    except HTTPError as http_err:
        #raise Exception 
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        #raise Exception
        print(f'Other error occurred: {err}')