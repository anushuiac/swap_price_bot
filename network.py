import requests
from requests.exceptions import HTTPError
from price import comma_sep

url_network = 'https://explorer.swap.foundation/api/networkinfo'
url_emission = 'https://explorer.swap.foundation/api/emission'
url_gecko = 'https://api.coingecko.com/api/v3/simple/price/'

def readable_hashrate(hashrate):
    i = 0
    units = ['H/S', 'KH/S', 'MH/S', 'GH/S', 'TH/S', 'PH/S' ]
    while hashrate > 1000:
        hashrate = hashrate/1000
        i += 1
    return '%.2f %s'%(hashrate, units[i])

def fetch_net_stats():
    try:
        response_network = requests.get(url_network, timeout=5)
        response_emission = requests.get(url_emission, timeout=5)
        response_coingecko = requests.get(url_gecko, params={'ids': 'swap',
                                 'vs_currencies': 'usd', 'include_market_cap':'true'}, timeout=5)

        json_network = response_network.json()
        json_emission = response_emission.json()
        json_gecko = response_coingecko.json()

        if json_network['status'] == 'success':
            # getting data
            hashrate = json_network['data']['hash_rate'] * 32
            height = json_network['data']['height']
            txs = json_network['data']['tx_count']
            tot_supply = 18400000
            available_supply = json_emission['data']['coinbase']/1e12
            difficulty = int(json_network['data']['difficulty']) * 32
            mc = json_gecko['swap']['usd_market_cap']

            # block_reward = (tot_supply - int(available_supply)) >> 18
            
            network_msg = '```Hash rate          : %s\nBlock height       : %s\nDifficulty         : %d\nTotal number of tx : %s\nTotal supply       : %s\nAvailable supply   : %s\nMarket Cap         : %s $```'%(readable_hashrate(hashrate),
                    comma_sep(height),
                    difficulty,
                    comma_sep(txs),
                    comma_sep(tot_supply),
                    comma_sep(int(available_supply)),
                    comma_sep(int(mc)),)
            return network_msg

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')