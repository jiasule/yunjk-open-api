# 使用说明

### 认证方式：HTTP basic 认证
创宇监控将提供api_id 以及用于生成密码的api_key。每个用户指定一个密钥，请严密保管。
所有的api的请求都要带上认证信息，认证信息5分钟有效。
basic auth 认证说明：

1. 使用BASIC AUTH认证。每次请求的密码均需要重新生成。
2. 密码由HMAC签名方式产生，hash方法为sha1，秘钥是由创宇监控提供的api_key。
3. 将接口参数按照参数名称字母顺序a-z排序，以&连接，得到参数字符串如a=1&b=2&c=3用于计算签名，
4. 最后将 app_id 作为用户，生成的签名作为认证密码。

示例：
```
API_ID = '582c10a9a54d75327c0dddee'
API_KEY = '3077f20de0644a92b0ae024519063d2b'

def make_sorted_data_string(data):
    for k, v in data.viewitems():
        if isinstance(v, unicode):
            data[k] = v.encode('utf-8')
    sorted_data = sorted(data.viewitems(), key=lambda x: x[0])
    sorted_string = urllib.urlencode(sorted_data)
    return urllib.unquote(sorted_string)

def make_headers(data, api_id, api_key):
    sorted_data =make_sorted_data_string(data)
    token = hmac.new(api_key, sorted_data, hashlib.sha1).hexdigest() # basic auth 的密码 
    sign = base64.b64encode('%s:%s'.format(api_id, token))
    headers = {'AUTHORIZATION': 'Basic %s' % sign}
    return headers

data = {
    'time': int(time.time())
    'url': 'http://www.baidu.com/',
    'type': 'HTTP',
    'name': 'test',
}
make_headers(data, API_ID, API_KEY)
# {'AUTHORIZATION': 'Basic 582c10a9a54d75327c0dddee:MjkwNGM0MzllZmY4N2RhMjVhNTk0ZDE4NzA5NmQ3MmI3NGQ4OGMwNQ=='}
```

curl 方式请求  
api_id 作为basic auth 的认证用户，通过hmac方式加密数据生成的字符串作为认证令牌  
token = hmac.new(api_key, sorted_data, hashlib.sha1).hexdigest() # basic auth 的密码   
如api_id = 582c10a9a54d75327c0dddee, token = MjkwNGM0MzllZmY4N2RhMjVhNTk0ZDE4NzA5NmQ3MmI3NGQ4OGMwNQ==

```
curl -u 582c10a9a54d75327c0dddee:MjkwNGM0MzllZmY4N2RhMjVhNTk0ZDE4NzA5NmQ3MmI3NGQ4OGMwNQ== 
-d 'name=aaa&time=&1490694173&type=HTTP&url=http://www.baidu.com' 
http://jk.yunaq.com/openapi/v1/task/create/
```


### 接口参数说明
* 所有请求都必须带有time参数，其值为字符串格式的UNIX时间戳
* 若是合作伙伴用户替普通用户执行创建任务等操作，除创建用户操作外，所有请求需带有username参数，如`username: 'test@knownsec.com`
* 其他说明：合作伙伴用户（如：PPB）会多一个创建用户接口



### 接口返回值说明
返回值说明

| code  | 含义                          |
| ----- | --------------------------- |
| 0     | 操作成功                        |
| 1000  | API内部错误                     |
| 1001  | 请求无 basic auth 认证           |
| 1002  | 无效的认证信息                     |
| 1003  | 认证信息过期                      |
| 1004  | 错误的app_id或app_key           |
| 1005  | 无效的认证签名                     |
|       |                             |
| 10001 | 请求必需的参数缺失或参数值无效，请修改参数       |
| 10002 | 不支持的监控类型或`type`参数缺失，请修改监控类型 |
| 10003 | 已达监控任务数上限，请申请提高监控任务数上限      |
| 10004 | 创建的监控任务已存在，请修改任务数据          |
| 20001 | 监控任务不存在或无权限获取该任务信息，请修改参数    |
| 20002 | 监控任务已经暂停，无实时数据              |
| 30001 | 参数不合法，请修改参数                 |
| 30002 | 告警组数量已达上限                   |
|       |                             |
| -1    | 无当前API调用权限                  |
| -2    | username参数缺失或参数不合法          |
| -3    | 用户已存在                       |

