## Flask+docker+Jenkins+GitHub CI部署  
***  
#### 1.docker安装  Jenkins安装
这段就省略不提了，好多可以参考
###  2.建立Flask应用
app.py:
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
```
这里使用gunicorn和gevent部署，所以需要额外的几个文件
gunicorn.conf.py
要在requirements.txt里面添加
```
gunicorn
gevent
```
```python
workers = 5 # 定义同时开启的处理请求的进程数量，根据网站流量适当调整
worker_class = "gevent" # 采用gevent库，支持异步处理请求，提高吞吐量
bind = "0.0.0.0:5000" # 监听IP放宽，以便于Docker之间、Docker和宿主机之间的通信
```

可以使用gunicorn命令来测试是否可以正确运行，命令如下：(windows不好使)
```shell
gunicorn app:app -c gunicorn.conf.py
```

接下来配置Dockerfile
```shell
FROM python:3
COPY requirements.txt ./
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]
```

### 3.在GitHub建立仓库，并将代码push到GitHub
### 4.配置Jenkins
  - 安装GitHub插件 GitHub Integration
  - 构建任务->构建一个自由风格的软件项目
  - 选择GitHub项目，在项目url中填写GitHub仓库的xxx.git
    <img src = "http://www.ywxisky.cn/usr/uploads/2019/10/1261176745.png" />
  - 选择丢弃旧的构建，可以节约空间
  - 源码管理选择git，填入git地址
  - 构建触发器选择GitHub hook trigger for GITScm polling 和轮询SCM，日程表内填写 H/30 * * * * （半个小时检查一次）
    <img src = "http://www.ywxisky.cn/usr/uploads/2019/10/3016321944.png" />
  - 构建环境选择 Delete workspace before build starts & Add timestamps to the Console Output
  - 在构建的地方选择执行shell 添加下面的命令，__要注意的是第一次构建需要注释掉前两行__

  ```shell
  docker rm -f flasktest
  docker rmi flaskimg
  docker build -t flaskimg .
  docker run -d -p 5000:5000 --name flasktest flaskimg
  ```

  <img src = "http://www.ywxisky.cn/usr/uploads/2019/10/1222461219.png" />

  - 保存后点击立即构建即可开始构建第一个项目

### 5.配置GitHub webhook
 - 前往GitHub 点击个人头像->settings->Developer settings->Personal access tokens生成一个新的token，选择repo和admin:repo_hook，将token复制下来
 - 打开Jenkins全局配置->GitHub ，添加GitHub服务器 并点开高级
  <img src = "http://www.ywxisky.cn/usr/uploads/2019/10/334256184.png" />
 - 第二步的时候类型选择Secert text，将刚刚复制的token填入Secert栏，添加即可
 - 进入GitHub仓库->settings->Webhooks 添加webhook，仅通知push，地址填写刚刚在Jenkins里为GitHub指定的hookurl，保存


 至此持续集成应该配置完毕了，后续配置一下Nginx即可使用！
