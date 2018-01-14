from stackapi import StackAPI
import json

SITE = StackAPI('stackoverflow')
search = SITE.fetch('search',order='desc',sort='activity',intitle='TypeError: unsupported operand type(s) for +: int and str')
print(search['items'][0]['link'])
