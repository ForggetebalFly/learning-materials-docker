import urllib.request, urllib.error, json
base='http://127.0.0.1:8040'
def req(path, method='GET', body=None):
    data=None if body is None else json.dumps(body).encode()
    request=urllib.request.Request(base+path,data=data,method=method,headers={'Content-Type':'application/json'})
    try: response=urllib.request.urlopen(request, timeout=10)
    except urllib.error.HTTPError as error: response=error
    text=response.read()
    return response.status, (json.loads(text) if 'application/json' in response.headers.get('Content-Type','') else text.decode()) if text else None
if __name__=='__main__':
    assert req('/health')[0]==200
    print('Health: 200 OK')
    code,item=req('/api/resources','POST',{'title':'Проверка Docker API','category':'Практика'})
    assert code==201 and item in req('/api/resources')[1]
    print('Create/read:',code,item)
    assert req('/api/resources/'+str(item['id']),'DELETE')[0]==204
    print('Delete: 204 OK')
    assert req('/api/resources','POST',{'title':'   '})[0]==400
    print('Empty title: 400 OK')
    assert req('/api/resources/'+str(item['id']),'DELETE')[0]==404
    print('Missing item: 404 OK')
    assert req('/')[0]==200
    print('Web page: 200 OK; all checks passed')
