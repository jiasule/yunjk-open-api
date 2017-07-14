# 创宇监控通用 API 使用文档

[TOC]

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

