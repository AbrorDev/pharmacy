from appbot.api import get_data

ADMINS = get_data(part_url='Telegran%20Users/filter', params={'is_admin':True}, part='tg_id')
OWNERS = get_data(part_url='Telegran%20Users/filter', params={'is_owner':True}, part='tg_id')