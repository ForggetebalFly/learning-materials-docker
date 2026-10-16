import sys,json
from pathlib import Path
from verify import req
state=Path('/tmp/task04-persistence.json')
if sys.argv[1]=='create':
    code,item=req('/api/resources','POST',{'title':'Сохранение данных после перезапуска','category':'Docker Volume'})
    assert code==201
    state.write_text(json.dumps(item),encoding='utf-8')
    print('Created:', item)
else:
    item=json.loads(state.read_text(encoding='utf-8'))
    assert item in req('/api/resources')[1]
    print('Persistence: OK; record remains after container recreation')
    print(item)
    assert req('/api/resources/'+str(item['id']),'DELETE')[0]==204
    print('Temporary record removed')
