android-boot-analytics
======================

a python script show time cost of android boot and some event

这是一个用于分析android启动过程的脚本，使用python抓取数据并把启动时的消耗打印出来


boot_time_reserch.py这个脚本是主要的，通过adb logcat -b events 来获取启动时的事件打印

需要python环境支持matplotlib,在ubuntu下可以一句 sudo apt-get install python-matplotlib搞定
