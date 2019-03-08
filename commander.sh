#！/usr/bin bash
# 添加不同子命令 模式

KEYS_FILE=$1
WITHOUT_TTL_FILE=$2
echo $KEYS_FILE
echo $WITHOUT_TTL_FILE

# 拿到没有过期时间的key列表
paste -d " " $KEYS_FILE $WITHOUT_TTL_FILE | grep -o ".*-1" | cut -d " " -f 1 > without_ttl
echo "keys without ttl has beed saved in without_ttl"

# 对without_ttl 文件查找具备频繁使用最通用前缀（由此看出，代码规范中对key的规范是多么重要，比如使用下划线_ 或者冒号: 进行分隔）
cat scankeys.txt | sort | cut -d ":" -f 1 | uniq -c | sort -nr | head  
