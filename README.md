# BaiduPCS-Go批量秒传与备份脚本生成

Python实现BaiduPCS-Go批量秒传脚本生成，并利用其批量秒传、资源备份与分享文件

# 引用：

https://github.com/iikira/BaiduPCS-Go

基本思想：根据手动秒传的方法，只要知道file_size和文件md5值，再根据自己意愿添加一个文件名，就可以根据云端已有数据在自己云盘中"拷贝"一份副本。

# 背景和思路

作者到目前有几十个云盘账号，文件管理起来比较麻烦，连账号切换都得靠Cookie Profile Switcher插件实现。再说，一个松鼠党必须时时保持警惕，应对账号被封资源丢失的痛苦。

秒传的原理是：通过检测文件大小和md5值，或者再加上其他如文件前256KB切片的md5值的信息，若云端有相同的文件，则直接进行云端拷贝。

BaiduPCS-Go的作者在新版本中实现如下功能：只需要知道file_size和md5，就可以实现在本地硬盘没有该文件下，但是云端别人已经上传过该文件时，进行虚拟秒传。

BaiduPCS-Go及其秒传功能的用法就不赘述了，均在github上。

举例：BaiduPCS-Go ru -length=<文件的大小> -md5=<文件的md5值> <网盘路径/文件名>

基于此思想，根据BaiduYunCacheFileV0.db文件含有文件目录，文件名，大小，md5等信息的原理，我们可以利用SQLite工具提取信息，配合Excel和其公式，制作一个如下类型的批处理文件：

```
BaiduPCS-Go ru -length=<size_1> -md5=<md5_1> <文件1>
BaiduPCS-Go ru -length=<size_2> -md5=<md5_2> <文件2>
BaiduPCS-Go ru -length=<size_3> -md5=<md5_3> <文件3>
...
pause
```
手动从db文件中提取信息并制作不难，但是繁琐。具体见[这里](https://github.com/silas1037/db_file2cmd_list/blob/master/手动提取生成批处理脚本.md)

直接利用下面的方法可以更快生成批处理脚本。

# 代码

[代码](https://github.com/silas1037/db_file2cmd_list/blob/v1.0/export_baiduyun_db.py)即可实现直接从db文件中提取信息并生成批处理脚本。

需要注意的是，生成的脚本是utf-8编码格式，可以通过[转码](#问题解决)的方法解决。

经本人测试，如果一个文件被两个账号上传过，则这个文件就进入了秒传许可的“高贵”行列。这时任意第三个账号均可以通过ru命令进行虚拟秒传，然后便可以被下载至本地。所以，我除了发布下载缓慢的[release](https://github.com/silas1037/db_file2cmd_list/releases/tag/v1.0)，还直接通过“秒传法”发布下面一个已经编译好的pe文件，尽情一试秒传的美妙。
```
BaiduPCS-Go ru -length=8547037 -md5=C4F76103263BB44BCE152058054365B2 export_baiduyun_db.exe
```
程序窗体示例：

![export_baiduyun.png](https://upload-images.jianshu.io/upload_images/12782677-7dcf64baa7946da3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


# 问题解决
## 针对字符乱码的解决方法
有时文件名有类似”†“的Unicode字符，即使保存为Unicode或者utf-8文档，在cmd中运行也是乱码，这时候就需要转码。

先将name.bat保存为utf-8编码的文档。

预先在cmd中输入chcp 65001可以无乱码运行utf-8文件。所以在name.bat同目录下建立另一个bat文件，输入：
```
chcp 65001
name.bat
pause
```
保存该bat为ANSI编码，双击运行即可调用name.bat。

如果需要保存输出到文本文档查看哪些秒传失败，代码如下：
```
chcp 65001
name.bat >>log.txt
pause
```
运行结束即可在log.txt中查看记录。

# 在本地资源管理器建立相同结构，并保存独立文件秒传信息

增加了两个脚本，可以产生两个批处理文件，利用批处理的md命令和echo建立文件命令建立类似云盘文件的文件目录结构。

[空目录产生命令](https://github.com/silas1037/db_file2cmd_list/blob/master/export_path.py)产生的脚本可以建立本地空目录，[文件建立命令](https://github.com/silas1037/db_file2cmd_list/blob/master/export_file.py)产生的脚本可以产生每一个文件均对应的“文件名.bat”。需要注意有两点：

1.产生的两个批处理脚本需要放在同一目录运行。
2.必须先运行[空目录产生命令](https://github.com/silas1037/db_file2cmd_list/blob/master/export_path.py)产生空目录，才能运行[文件建立命令](https://github.com/silas1037/db_file2cmd_list/blob/master/export_file.py)建立对应文件。
3.均需要预输入` chcp 65001 `进行调用。
