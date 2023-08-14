#!/bin/bash

# 提示用户输入日期
echo "请输入日期（例如：2023-08-10）："
read current_date
# 提示用户输入的天数
echo "请输入向前爬取的天数（例如：5）："
read num_loops

# 获取当前日期
# current_date=$(date +%Y-%m-%d)
# current_date="2023-03-15"
# 循环次数
# num_loops=3  # 或者你希望的循环次数

for ((i=0; i<$num_loops; i++)); do
    # 计算昨天的日期
    case $(uname) in
        "Darwin")
            previous_date=$(date -v -1d -j -f "%Y-%m-%d" "$current_date" "+%Y-%m-%d")
            ;;
        "Linux")
            previous_date=$(date -d "yesterday $current_date" "+%Y-%m-%d")
            ;;
        *)
            echo "Unsupported operating system"
            exit 1
            ;;
    esac
    # 执行 Python 脚本并传入日期参数
    scrapy runspider ./scrapy/szggzy_interface.py -a startDate="$current_date" -a endDate="$current_date" >> ./scrapy/logs/scrapy.log

    # 休眠 5 分钟
    sleep 300

    # 当前日期更新为昨天的日期
    current_date=$previous_date
done