
import pandas as pd

import requests

def get_dune_data(query_id, dune_key):
    query_link = f'https://api.dune.com/api/v1/query/{query_id}/execute'
    headers = {'x-dune-api-key': dune_key}
    data = '{}'
    query_execution_link = requests.post(query_link, headers=headers, data=data)
    query_execution_id = query_execution_link.json()['execution_id']
    status_link = f'https://api.dune.com/api/v1/execution/{query_execution_id}/status'
    status_query = requests.get(status_link, headers=headers, data=data)
    while status_query.json()['state'] != 'QUERY_STATE_COMPLETED':
        time.sleep(10)
        status_query = requests.get(status_link, headers=headers, data=data)

    result_link = f'https://api.dune.com/api/v1/execution/{query_execution_id}/results'
    result_query = requests.get(result_link, headers=headers, data=data)
    results_df = pd.DataFrame(result_query.json()['result']['rows'])
    results_df = results_df.rename(columns={'amount': 'amount', 'wallet': 'user', 'ethdebt': 'ethdebt'})
    return results_df