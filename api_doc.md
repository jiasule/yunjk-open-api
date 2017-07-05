# 创宇监控通用 API 使用文档

[TOC]

## 概述

API 域名：http://jk.yunaq.com

开通方式：
1. 注册成为知道创宇通行证用户，并使用该账号登录进入创宇监控系统。
2. 申请 API 调用密钥。

### 认证：HTTP basic 认证
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

### 接口列表

#### 监控任务

##### 创建监控任务

- URI: `/openapi/v1/task/create/`，必须包括末尾/

- method: `POST`

- 参数:

  | 参数名       | 类型     | 是否必须 | 说明                                       |
  | --------- | ------ | ---- | ---------------------------------------- |
  | name      | string | 是    | 任务名称                                     |
  | type      | string | 是    | 任务类型，该参数值需是`HTTP`                        |
  | url       | string | 是    | 监控任务的url。注意，需以`http:// 或 https://`开头     |
  | time      | int    | 是    | 时间戳                                      |
  | gid       | string | 否    | 任务告警组的组id，可从添加告警组接口获取到gid。不传该参数，则默认不发送告警。 |
  | server_ip | string | 否    | url对应的源站IP，适用于使用了CDN访问的URL地址。参数值需是有效的公网 IP 地址。 若传该参数，则监控IP地址所映射的源站服务。 |

- 返回结果：

  ```
  # 操作失败
  {
    "msg": "请求必需的参数缺失或参数值无效，请修改参数",
    "code": 10002
  }

  # 操作成功
  {
    "msg": "创建监控任务成功",
    "code": 0,
    "data": {
      "tid": "4e383e305c12498b8e14aa44e46425dc"
    }
  }
  ```

##### 

##### 获取任务列表
* URI: `/openapi/v1/task/list/`

* 方法：`GET`

* 参数:

  | 参数名    | 类型   | 是否必须 | 说明      |
  | ------ | ---- | ---- | ------- |
  | offset | int  | 否    | 任务列表偏移量 |
  | time   | int  | 是    | 时间戳     |

* 返回：每次请求最多返回10条数据。
```
{
  "msg": "操作成功",
  "code": 0,
  "data": {
    "total": 13,  // 任务总数
    "tasks": [ // 任务列表
      {
        "tid": "d9c686ab4e2d4928a79dc171fce41b03",
        "is_stop": false, // 任务是否暂停
        "url": "sincerity.bbbkm.com",
        "name": "name"
      },
      ...
    ]
  }
},
```

##### 开启暂停任务
* URI: `/openapi/v1/task/<tid>/switch/`

* 方法：`POST`

* 参数:

  | 参数名    | 类型     | 是否必须 | 说明                        |
  | ------ | ------ | ---- | ------------------------- |
  | action | string | 是    | 暂停或开启任务：可选值为[start, stop] |
  | time   | int    | 是    | 时间戳                       |
  | tid    | string | 是    | 任务id，嵌入在uri里面             |

* 返回结果：
```
{
  "msg": "修改任务状态成功",
  "code": 0,
  "data": {
    "tid": "c9d96df6410e4bdd8f76dce069432260",
    "is_stop": false //是否暂停，表示任务状态
  }
}
```

##### 删除监控任务
* URI: `/openapi/v1/task/<tid>/delete/` 

* method: `POST`

* 参数:

  | 参数名  | 类型     | 是否必须 | 说明            |
  | ---- | ------ | ---- | ------------- |
  | tid  | string | 是    | 任务id，嵌入在uri里面 |
  | time | string | 是    | 时间戳           |

* 返回结果：
```
  {
    "msg": "删除监控任务成功",
    "code": 0,
    "data": {
      "tid": "4e383e305c12498b8e14aa44e46425dc"
    }
  }
```



#### 监控结果

##### 获取常规监控结果（当日，昨日，最近7日）

* URI: `/openapi/v1/task/<tid>/result/`

* 方法：`GET`

* 参数:

  | 参数名           | 类型     | 是否必须 | 说明            |
  | ------------- | ------ | ---- | ------------- |
  | tid           | string | 是    | 任务id，嵌入在uri里面 |
  | avg_resp_time | string | 否    | 表示平均响应时间      |
  | usable_rate   | string | 否    | 表示可用率         |
  | error_percent | string | 否    | 表示错误占比        |
  | time          | string | 是    | 时间戳           |

  其他说明：avg_resp_time, usable_rate, error_percent需含有其一，使用时只需要传需要的数据项对应的参数即可。以下是参数的可选值

  - 0: 当日数据
  - 1: 昨日数据
  - 7: 最近7日数据

* 参数样例
```javascript
{
    "avg_resp_time": 0,   // 获取当日每小时平均响应时间数据
    "usable_rate": 1,    // 获取昨日每小时可用率数据
    "error_percent": 7   // 获取最近7日的平均异常占比数据
}
```

返回结果：

```
{
  "msg": "操作成功",
  "code": 0,
  "data": {
    "avg_resp_time": [{...}, {...}],
    "usable_rate": [{...}, {...}],
    "error_percent": 0.0667
```

##### 获取单个任务的实时监控数据（最近一次监控）

* URI: `/openapi/v1/task/<tid>/realtime_res/`

* method：`GET`

* 参数

  | 参数   | 类型     | 是否必须 | 说明            |
  | ---- | ------ | ---- | ------------- |
  | tid  | string | 是    | 任务id，嵌入在uri里面 |
  | time | string | 是    | 时间戳           |

* 返回结果：data数据含义

  | 数据字段          | 含义                                       | 示例                                       |
  | ------------- | ---------------------------------------- | ---------------------------------------- |
  | status        | 当前状态。0表示正常，1表示警告，2表示故障, 3表示未知            | 0                                        |
  | avg_resp_time | 平均响应时间，单位 ms。（当status为3，avg_resp_time为0） | 185.25                                   |
  | node_resp     | 各个探测节点的具体响应时间。                           | { "重庆市联通": 183.25, "成都市电信": 183.25, ... } |

```
{
  "msg": "操作成功",
  "code": 0,
  "data": {"status": 0, "avg_resp_time": 185.25, "node_resp": { "重庆市联通": 183.25, "成都市电信": 183.25}}
}
```



##### 获取多个任务的实时监控数据（最近一次监控）

- URI：/openapi/v1/task/multi_realtime_res/

- method：POST

- 参数 

  | 参数   | 类型     | 是否必须 | 说明                |
  | ---- | ------ | ---- | ----------------- |
  | tids | list   | 是    | 需要获取实时状态数据的任务id列表 |
  | time | string | 是    | 时间戳               |

  返回结果：返回json对象，key是tid，value是该tid对应的状态数据。

  | 字段            | 含义                                       | 示例                                       |
  | ------------- | ---------------------------------------- | ---------------------------------------- |
  | status        | 当前状态。0表示正常，1表示警告，2表示故障, 3表示未知            | 0                                        |
  | avg_resp_time | 平均响应时间，单位 ms。（当status为3，avg_resp_time为0） | 185.25                                   |
  | node_resp     | 各个探测节点的具体响应时间。                           | { "重庆市联通": 183.25, "成都市电信": 183.25, ... } |

  ```

  {
    "msg": "操作成功",
    "code": 0,
    "data": {
  	"tid1": {"status": 0, "avg_resp_time": 185.25, "node_resp": { "重庆市联通": 183.25, "成都市电信": 183.25}},
  	"tid2": {"status": 0, "avg_resp_time": 185.25, "node_resp": { "重庆市联通": 183.25, "成都市电信": 183.25}},
  	...
    }
  }
  ```






##### 用户任务状态概览

- URI：/openapi/v1/task/user_summary/

- method：GET

- 参数 

  | 参数       | 类型     | 是否必须 | 说明                                       |
  | -------- | ------ | ---- | ---------------------------------------- |
  | username | string | 否    | 无该参数，则返回api_id 对应的用户的任务状态概览数据;有该参数，且api_id含有操作其他用户任务的权限，则返回username对应用户的任务状态概览数据 |
  | time     | string | 是    | 时间戳                                      |

- 返回样例

  ```

  {
    "msg": "操作成功",
    "code": 0,
    "data": {
  	"0": ["857cd6aac3574d8d99243f84567fc5da", ...]  // 正常状态的任务id列表
  	"1": ["857cd6aac3574d8d99243f84567fc5da", ...]  // 警告状态
  	"2": ["857cd6aac3574d8d99243f84567fc5da", ...]  // 故障状态
  	"3": []              							// 未知状态
    }
  }
  ```

  ​


#### 告警组

##### 创建告警组

- URI: `/openapi/v1/user/alert_group/`

- method：`POST`

- 在用户账号下创建一个告警组，一个告警组同时支持设置邮箱接收邮件告警，和设置手机号接收短信告警。

- 参数

  | 参数          | 类型     | 是否必须 | 说明                       |
  | ----------- | ------ | ---- | ------------------------ |
  | name        | string | 否    | 告警分组名，若无此参数则为默认分组名：默认告警组 |
  | alert_email | string | 否    | 接收告警邮件的邮箱地址              |
  | alert_phone | string | 否    | 接收告警短信的手机号               |

  参数 alert_email 和 alert_phone 需至少设置一项。

- 返回结果：

  - 调用成功，返回告警组id，可用于创建任务时设置告警

  ```javascript
  {
    code: 0, 
    data: {
      gid: 'xxxxxxxxx'   // 告警组id
    }
  }
  ```

  - 调用失败，返回对应提示信息

  ```javascript
  {
    code: 10001, //非0 
    msg: 'xxxxxxxxx'  
  }
  ```

##### 查询告警组列表

- URI: `/openapi/v1/user/alert_group/`

- method：`GET`

- 参数：无需参数 

- 返回结果：

  - 调用成功，返回告警组列表

  ```javascript
  {
    code: 0, 
    data: {[
     {
       name: "xxxx", 
       gid: "xxxx", 
       phones: ["13208190981"...],
       emails: ["test@knownsec.com"...],
     },
      ...
    ]}
  }
  ```

  - 调用失败，返回对应提示信息

  ```javascript
  {
    code: 10001, //非0 
    msg: 'xxxxxxxxx'  
  }
  ```

#### 其他

##### 创建用户接口

- URI: `/openapi/v1/user/create/`

- method：`POST`

- 在系统内创建一个用户，若用户已经存在，则无需重复创建。

- 参数

  | 参数    | 类型     | 是否必须 | 说明       |
  | ----- | ------ | ---- | -------- |
  | email | string | 是    | 被创建的用户邮箱 |

- 返回结果：

  * 调用成功：code=0

  ```
  {
    "data": {},
    "code": 0,
  }
  ```

  * 调用失败：code != 0，msg 为对应提示

  ```
  {
    "msg": "xxxxxxx",
    "code": -1/-2/-3,
  }
  ```

  ​

  ​

  ​

