### 执行爬虫
- Python 脚本执行
  `scrapy runspider szggzy_interface.py -a startDate='2023-06-16' -a endDate='2023-06-16' >> ./scrapy.log`
- shell 脚本执行
  - 询问用户输入
    ```shell
    ./scrapy_loop.sh
    请输入日期（例如：2023-08-10），回车默认为昨天：
    2023-02-14
    请输入向前爬取的天数（例如：5），回车默认为1：
    2
    ```
  - 参数输入
    ```shell
    ./scrapy_loop.sh auto 2023-06-10 5
    ```
  - nohup 后台执行
    ```shell
    nohup ./scrapy_loop.sh auto 2023-08-08 50 > /dev/null 2>&1 &
    ```

### 采购公告
https://www.szggzy.com/jygg/list.html


### client
- 本地开发
```
yarn dev
```
http://localhost:8080/#/purchase/list
http://localhost:8080/#/purchase/detail?contentId=1863594

- 部署
```
yarn deploy:prod
```

### web server
- 本地开发
```
yarn start:dev
```
http://localhost:8000/announcement/list

- 部署
```
yarn start
# 后台运行
nohup yarn start > /dev/null 2>&1 &
```