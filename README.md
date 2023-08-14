### 执行爬虫
- Python 脚本执行
  `scrapy runspider szggzy_interface.py -a startDate='2023-06-16' -a endDate='2023-06-16' >> ./scrapy.log`
- shell 脚本执行，提示输入
  ```shell
  ./scrapy_loop.sh
  请输入日期（例如：2023-08-10）：
  2023-02-14
  请输入向前爬取的天数（例如：5）：
  2
  ```
- shell 脚本根据参数自动执行
  ```shell
  ./scrapy_loop.sh auto 2023-06-10 5
  ```

### 采购公告
https://www.szggzy.com/jygg/list.html


### 本地开发
- 启动 client 平台
yarn dev
http://localhost:8080/#/purchase/list
http://localhost:8080/#/purchase/detail?contentId=1863594

- 启动 web server
yarn start:dev 
http://localhost:3000/announcement/list
