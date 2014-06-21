##申明
* 代码主要来源于：[https://github.com/fatiherikli/worldcup](https://github.com/fatiherikli/worldcup)
* 目测不能给上游贡献代码，所以没有fork。

##修改内容
* 依赖关系：把humanize、dateutil.parser、dateutil.tz替换为arrow。
* 语言：并将英文修改为中文。

##使用说明
1. Clone代码：
    * `git clone https://github.com/Masakichi/worldcup.git`
    * `cd worldcup`

2. 安装依赖：
`pip install -r requirements.txt`

3. 运行：
    * `python worldcup.py`
    * `python worldcup.py today`
    * `python worldcup.py tomorrow`
    
##效果图
![worldcup](http://ww3.sinaimg.cn/large/4b31c31egw1ehlwgecf3fj20ln0h33zz.jpg)

![worldcup-today](http://ww1.sinaimg.cn/large/4b31c31egw1ehlwh7y31kj20ln0h30up.jpg)

##数据来源
* [http://worldcup.sfg.io/matches/](http://worldcup.sfg.io/matches/)
* [https://github.com/estiens/world_cup_json](https://github.com/estiens/world_cup_json)

##TODO
* 增加分组情况查询。
* 增加各队查询。