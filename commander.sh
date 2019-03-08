#！/usr/bin bash
# 添加不同子命令 模式

KEYS_FILE=$1
WITHOUT_TTL_FILE=$2
echo $KEYS_FILE
echo $WITHOUT_TTL_FILE
return 0
paste -d " " $KEYS_FILE $WITHOUT_TTL_FILE | grep -o ".*-1" | cut -d " " -f 1 > without_ttl
echo "keys without ttl has beed saved in without_ttl"
