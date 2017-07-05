# 创宇监控一次性探测 API 使用文档

用户可通过一次性API接口，对指定的目标进行实时http探测或者ping探测。



##### 下发探测任务接口：

通过调用该接口，对探测对象下发探测任务。

* URI: `/openapi/v1/once_task/create/`

* 方法：`POST` 

* 参数：

  | 参数名  | 类型     | 是否必须 | 说明                     |
  | ---- | ------ | ---- | ---------------------- |
  | data | string | 是    | json结构的数组，通过序列化生成的字符串。 |


  data原始数据是一个数组，其元素是一个对象，其参数如下：


| 参数名       | 类型     | 是否必须 | 说明                                       |
| --------- | ------ | ---- | ---------------------------------------- |
| type      | string | 是    | 探测类型，参数值范围：['HTTP', 'PING']              |
| target    | string | 是    | 探测目标。若参数type为HTTP，target需以`http:// 或 https://`开头的链接;若参数type为ping，target需要是域名或者有效公网IP地址。 |
| server_ip | string | 否    | 若参数type为HTTP，则server_ip为target参数值所对应的源站IP的地址。 |

示例

```
# curl 请求
curl -H "application/x-www-form-urlencoded" --data 'data=[{"type": "http", "target": "http://hao.cnfol.com/index.html"}, {"type": "ping", "target": "hao.cnfol.com"}]' http://localhost:8080/openapi/v1/once_task/create

# Python 代码请求
data = [
    {'target': 'http://hao.cnfol.com/index.html', 'type': 'http', 'server_ip': '222.23.2.23'},
    {'target': 'hao.cnfol.com', 'type': 'ping'}
]
data = json.dumps(data)
requests.post('http://jk.yunaq.com/openapi/v1/once_task/create', data={'data':data})
```



* 返回：每次请求最多返回10条数据。
```
{
  "msg": "操作成功",
  "code": 0,
  "data": [ 下发的探测任务列表
      {
        "target": 'xxxxxxxx', // 用户传递的target参数
        "tid": "d9c686ab4e2d4928a79dc171fce41b03",  // 该target参数对应的tid，可根据该tid查询探测结果
      },
      ...
    ]
  }
}
```

##### 查询探测结果接口

通过调用该接口，查询已下发探测任务的结果数据。

- URI: `/openapi/v1/once_task/result/`

- 方法：`GET`

- 参数：

  | 参数名  | 类型   | 是否必须 | 说明                          |
  | ---- | ---- | ---- | --------------------------- |
  | tids | list | 是    | 需要查询的任务的tid列表。tid由下发任务接口返回。 |

示例

```
# curl
curl http://jk.yunaq.com/openapi/v1/once_task/result?tids=dfdf7e44fb694666a4904a372406d3ff&tids=dfdf7e44fb694666a4904a372406d3f0

# python
request.get('curl http://jk.yunaq.com/openapi/v1/once_task/result?tids=dfdf7e44fb694666a4904a372406d3ff&tids=dfdf7e44fb694666a4904a372406d3f0')
```

* 返回结果

  以下所有涉及时间的返回值参数都为ms

```
{
  "msg": "操作成功",
  "code": 0,
  "data": [
    {                                                    // HTTP 探测结果说明
      "tid": "a2e0562ba30c480ab514a46123cc9f77",         // 下发任务的tid，与参数值一致
      "resp_avg": 191.67,                                // 平均响应时间
      "detail": [                                        // 该任务在各个探测节点的详细数据
        {
          "area": "四川省电信",                           // 探测节点的地理位置和ISP运营商
          "ip": "220.167.109.71",                        // 探测目标的响应IP
          "resp_time": 119,                              // 探测请求的响应时间
          "download_time": 41.25,                        // 探测请求的内容下载时间
          "download_speed": "",                          // 探测请求的下载速度，单位为MB/s
          "status_code": 200,                            // 探测请求HTTP状态码
          "dns_time": 6.33                               // 探测请求的dns解析时间
        },
        ...
      ]
    }，
    {                                                    // PING 探测结果说明
      "tid": "90663d9a18034ca5a16215146e982fd7",         // 下发任务的tid，与参数值一致
      "resp_avg": 44.16,                                 // 平均响应时间
      "detail": [                                        // 该任务在各个探测节点的详细数据
        {
          "ip": "58.223.166.231",                        // ping 探测请求的响应IP
          "resp_time": 39.71,                            // ping 探测请求的响应IP
          "loss_rate": 0.25,                             // ping探测的丢包率，0.25表示丢包率为25%
          "area": "武汉市电信"                            // 探测节点的地理位置和ISP运营商
        },
        ...
      ]
    }
      ...
  ]
}
```



