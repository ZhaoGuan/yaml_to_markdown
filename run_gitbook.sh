#!/bin/sh
host=$1
# 指定记录服务的host
sed -i 's/0.0.0.0:8000/'"${host}"'/g' ./module/recording.html
# 关闭之前的gitbook服务
# shellcheck disable=SC2009
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
# shellcheck disable=SC2164
cd md_cases
gitbook install
#nohup gitbook serve &
gitbook build
