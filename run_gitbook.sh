#!/bin/sh
# 关闭之前的gitbook服务
ps -ax | grep gitbook | grep -v grep | awk '{ print $1 }' | xargs kill -2
# 创建md_cases文件夹
rm -rf ./md_cases
mkdir ./md_cases
sleep 2
# shellcheck disable=SC2225
python3 ./module/to_markdown.py
# 复制文件
cp ./module/recording.html ./md_cases
cp ./module/recording.html ./md_cases
cp ./module/README.md ./md_cases
cp ./module/book.json ./md_cases
cd md_cases
gitbook install
nohup gitbook serve &
