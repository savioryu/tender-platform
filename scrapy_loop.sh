#!/bin/bash

# 函数：获取前一天的日期
get_previous_date() {
    case $(uname) in
        "Darwin")
            date -v -1d -j -f "%Y-%m-%d" "$1" "+%Y-%m-%d"
            ;;
        "Linux")
            date -d "yesterday $1" "+%Y-%m-%d"
            ;;
        *)
            echo "Unsupported operating system"
            exit 1
            ;;
    esac
}

if [ "$1" != "auto" ]; then
    # 询问用户输入日期
    echo "请输入日期（例如：2023-08-10），回车默认为昨天："
    read current_date_input

    # 提示用户输入的天数
    echo "请输入向前爬取的天数（例如：5），回车默认为1："
    read num_loops_input
else 
    current_date_input=$2
    num_loops_input=$3
fi

# 如果用户输入为空，则使用默认值（昨天）
if [ -z "$current_date_input" ]; then
    current_date=$(get_previous_date $(date +\%Y-\%m-\%d))
else
    current_date="$current_date_input"
fi

# 循环次数
# 如果用户输入为空，则使用默认值（1）
if [ -z "$num_loops_input" ]; then
    num_loops_input=1
else
    num_loops_input="$num_loops_input"
fi


for ((i=0; i<$num_loops_input; i++)); do
    echo "当前日期：$current_date"
    # 执行 Python 脚本并传入日期参数
    scrapy runspider ./scrapy/szggzy_interface.py -a startDate="$current_date" -a endDate="$current_date" >> ./scrapy/logs/scrapy.log
    # 倒计时时长
    countdown_seconds=300
    # 清空行
    clear_line="\033[2K"
    while [ $countdown_seconds -gt 0 ]; do
        echo -ne "$clear_line\r等待倒计时: $countdown_seconds 秒"
        sleep 1
        ((countdown_seconds--))
    done

    # 当前日期更新为昨天的日期
    current_date=$(get_previous_date "$current_date")
    echo
done