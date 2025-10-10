# 图片重命名脚本
# 将IMG_xxxx.jpg重命名为对应的书名

$sourceDir = "e:\books\photo_jpg"
$books = @(
    "红楼梦",
    "红楼梦",
    "红楼梦",
    "百年孤独",
    "霍乱时期的爱情",
    "月亮与六便士",
    "月亮与六便士",
    "活着",
    "瓦尔登湖",
    "挪威的森林",
    "围城",
    "围城",
    "童年·在人间·我的大学",
    "童年·在人间·我的大学",
    "如何阅读一本书",
    "孽子",
    "富爸爸穷爸爸",
    "小狗钱钱",
    "巨人的陨落",
    "把时间当作朋友",
    "把时间当作朋友",
    "查令十字街",
    "毛姆传",
    "毛姆传",
    "汉谟拉比法典",
    "真相",
    "睡眠革命",
    "刀锋",
    "人性的枷锁",
    "人性的枷锁",
    "不能承受的生命之轻",
    "不能承受的生命之轻",
    "三十七度二",
    "1%法则",
    "1%法则",
    "1%法则",
    "未知书籍_1"
)

# 获取所有图片文件并排序
$images = Get-ChildItem -Path $sourceDir -Filter "IMG_*.jpg" | Sort-Object Name

if ($images.Count -ne $books.Count) {
    Write-Host "警告：图片数量($($images.Count))与书名数量($($books.Count))不匹配！"
}

# 创建书名计数器
$bookCounter = @{}

# 重命名文件
for ($i = 0; $i -lt $images.Count; $i++) {
    $oldPath = $images[$i].FullName
    $bookName = $books[$i]
    
    # 统计该书名出现次数
    if ($bookCounter.ContainsKey($bookName)) {
        $bookCounter[$bookName]++
        $newName = "${bookName}_$($bookCounter[$bookName]).jpg"
    } else {
        $bookCounter[$bookName] = 1
        $newName = "${bookName}.jpg"
    }
    
    $newPath = Join-Path -Path $sourceDir -ChildPath $newName
    
    Write-Host "重命名: $($images[$i].Name) -> $newName"
    Rename-Item -Path $oldPath -NewName $newName -ErrorAction Stop
}

Write-Host "`n重命名完成！"
Write-Host "共处理 $($images.Count) 个文件"
