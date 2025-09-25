import requests
from time import sleep
from bs4 import BeautifulSoup
import re

pattern = r'0x[a-fA-F0-9]{40}'


def scrape_block(blocknumber, page):
    # the URL of the web page that we want to get transaction data
    api_url = "https://etherscan.io/txs?block=" + str(blocknumber) + "&p=" + str(page)
    # HTTP headers used to send a HTTP request
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'}
    # Pauses for 0.5 seconds before sending the next request
    sleep(0.5)
    # send the request to get data in the webpage
    response = requests.get(api_url, headers=headers)
    # get the transaction table from the response data we get
    txs = BeautifulSoup(response.content, 'html.parser').select('table.table-hover tbody tr')
    for row in txs:
        tx = extract_transaction_info(row)
        print("transaction of ID:", tx['hash'], "block:", tx['block'], "from address", tx['from'], "toaddress", tx['to'], "transaction fee", tx['fee'])


def extract_transaction_info(tr_element):
    try:
        # Extract transaction hash
        tx_hash = tr_element.select_one('.myFnExpandBox_searchVal').text.strip()

        # Extract transaction type
        tx_type = tr_element.select_one('span[data-title]').text.strip()

        # Extract block number
        block = tr_element.select_one('td:nth-child(4) a').text.strip()

        # Extract timestamp
        timestamp = tr_element.select_one('td.showAge span')['data-bs-title']

        # Extract from address
        from_element = tr_element.select_one('td:nth-child(8) a')
        from_addr = tr_element.select_one('td:nth-child(8) a').text.strip()
        if 'data-bs-title' in from_element.attrs:
            from_full = from_element['data-bs-title']
        else:
            # Try to get from span if <a> doesn't have it
            from_span = from_element.select_one('span[data-bs-title]')
            from_full = from_span['data-bs-title'] if from_span else from_addr
        from_address = re.search(pattern, from_full).group()

        # Extract to address
        to_element = tr_element.select_one('td:nth-child(10) a')
        to_addr = to_element.text.strip()
        # to_full = to_element['data-bs-title'] if 'data-bs-title' in to_element.attrs else to_addr
        if 'data-bs-title' in to_element.attrs:
            to_full = to_element['data-bs-title']
        else:
            # Try to get from span if <a> doesn't have it
            to_span = to_element.select_one('span[data-bs-title]')
            to_full = to_span['data-bs-title'] if to_span else to_addr
        to_address = re.search(pattern, to_full).group()

        # Extract value
        value = tr_element.select_one('.td_showAmount').text

        # Extract transaction fee
        tx_fee = tr_element.select_one('.showTxnFee').text.strip()

        # Extract gas price if available
        gas_price = tr_element.select_one('.showGasPrice')
        gas_price = gas_price.text.strip() if gas_price else None

        return {
            'hash': tx_hash,
            'type': tx_type,
            'block': block,
            'timestamp': timestamp,
            'from': from_address,
            'to': to_address,
            'value': value,
            'fee': tx_fee,
            'gas_price': gas_price
        }

    except Exception as e:
        print(f"Error extracting transaction info: {e}")
        return None


if __name__ == "__main__":  # entrance to the main function
    scrape_block(15479087, 1)