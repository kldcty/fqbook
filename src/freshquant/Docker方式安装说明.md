# 番茄量化Pro版

## FQ量化环境Docker安装部署指南

由于在Windows Docker Desktop上使用，因此一些命令遵循Windows的风格。

### Windows开启Linux子系统

首先确认CPU的虚拟化功能已开启。打开任务管理器，切换到性能的CPU选项卡，查看CPU虚拟化是否已开启。

![](CPU虚拟化.jpeg)

如果未开启，请进入电脑的BIOS设置开启虚拟化。根据电脑主板的不同，请自行找到相应的配置选项进行修改。

分别开启电脑的虚拟化平台和Linux子系统服务，在Powershell中执行以下命令。

```
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -All -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -All -NoRestart
```

也可以使用以下dism命令在cmd中开启虚拟化和Linux子系统。

```
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

安装过程中如果需要重启电脑，请按照提示操作。

如果还没有安装WSL，用下面的命令安装WSL。

```
winget install Microsoft.WSL
```

或者是升级到WSL的最新版本。

```
winget upgrade Microsoft.WSL
```

更新WSL核心到最新版本（效果和winget upgrade Microsoft.WSL一样）。

```
wsl --update
```

查看确认WSL使用版本2。

```
wsl --status
```

![](wsl_status.jpeg)

如果默认版本不是2，请设置WSL的默认版本。

```
wsl --set-default 2
```

安装WSL的Ubuntu版本。

```
wsl --install -d Ubuntu
```

或者是用这个命令安装wsl的ubuntu（效果和wsl --install -d ubuntu一样）

```
winget install Canonical.Ubuntu
```

一般一个命令不顺畅的话，就试试另一个可替代命令。

### 安装Windows Docker Desktop

从Docker官网下载Docker Desktop并安装，建议基于WSL2进行安装。这种方式比之前的版本更稳定。安装完成后，系统托盘区会出现一个船形图标，双击即可打开Docker Desktop。

也可以用下面的命令来安装

```
winget install Docker.DockerDesktop
```

![](windows_docker_desktop.jpeg)

至此，Docker环境已经安装完成。

请记得配置镜像加速器，推荐使用阿里云的镜像加速器。需要注册并登录阿里云账号，在容器镜像服务中获取镜像加速器地址。务必配置加速器，否则镜像拉取速度会非常慢。

找到齿轮按钮打开设置。

![](Docker代理配置.jpeg)

在设置中添加镜像加速器地址，可以加速下载。

也可以使用其他加速地址，例如：

```
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "registry-mirrors": [
    "https://dockerproxy.com",
    "https://mirror.baidubce.com",
    "https://docker.m.daocloud.io",
    "https://docker.nju.edu.cn",
    "https://docker.mirrors.sjtug.sjtu.edu.cn"
  ]
}
```

接下来开始安装量化系统。

### 设置环境变量

在环境变量中设置以下变量，系统运行时会用到它们。

- TDX_HOME：指向通达信的安装目录。
- FQ_PERSIST_DIR：指向量化系统数据存放目录（自己提前建好目录，保证目录存在）。

```
set TDX_HOME=E:\new_haitong
set FQ_PERSIST_DIR=E:\FQ_PERSIST_DIR
setx TDX_HOME E:\new_haitong
setx FQ_PERSIST_DIR E:\FQ_PERSIST_DIR
```

前两句是临时设置当前命令环境的变量，关闭窗口后设置会丢失。后两句是永久设置环境变量，下次打开时环境变量仍然存在。

### 执行部署

在源码的根目录运行脚本。

```
deploy.bat
```

提示选择通达信的目录。因为软件中需要读取通达信数据，这里输入通达信的安装目录。

![](通达信目录.jpeg)

如果环境变量已经设置正确，这里直接回车使用默认值即可。

提示选择数据存放目录。

![](数据存放目录.jpeg)

同样，如果环境变量已经设置正确，直接回车使用默认值即可，同时确保目录存在。

提示是否需要构建rear镜像，第一次安装时选择Y，如果已经构建过且代码未更新，可以选择N。

![](build_rear.jpeg)

等待rear镜像构建完成。如果遇到卡住的情况，一般是网络问题，建议使用代理。

另外有两个脚本build_rear.bat和build_web.bat，可以在运行deploy.bat前先运行这两个脚本构建镜像，这样运行deploy.bat时可以选择N。

询问是否需要构建web镜像，第一次或前端代码有更新时选择Y，否则选择N。

![](build_web.jpeg)

等待web镜像构建完成。

接下来脚本会在Docker中逐个部署容器。只需等待部署完成。

部署完成后，在浏览器中打开http://127.0.0.1:10003，这是自动化任务管理端。

切换到automation页面，打开自己要允许的任务。

![](automation.png)

这样每天会定时运行这些任务。

此时数据库中还没有数据。可以切换到Jobs页面，点击jobSaveStockData，点击Raunchpad，点击最右下角的Launch Run。这样就开始下载股票数据了。查看日志如图所示即为正常。

![](launch_run.jpeg)

同样方法，运行jobSaveIndexData，jobSaveFutureData，jobSaveEtfData，jobSaveBondData，下载这几个历史数据。

至此，系统安装完成。在浏览器中打开http://127.0.0.1，可以访问系统的Dashboard。

## 自动任务说明

打开地址[http://127.0.0.1:10003](http://127.0.0.1:10003)，打开标签页Automation，在上面可以开启或者关闭自动任务。目前的任务有以下这些。

| 名称                                  | 说明                                      | 建议   |
| ----------------------------------- | --------------------------------------- | ---- |
| default_automation_condition_sensor | 默认的自动化sensor，要asset的自动物化就要打开这个开关。       | 务必打开 |
| job_clean_db_schedule               | 每天定时清理数据库中不需要永久保存的数据                    | 打开   |
| jobBackfillOrder_schedule           | 补单，例如昨天委托但未成交的订单，今天是否继续委托。如果开启，今天会继续委托。 | 按需打开 |
| jobReverseRepo_schedule             | 逆回购任务，每天收盘前把多余的资金进行逆回购，保留2W现金。          | 按需打开 |
| jobSaveBondData_schedule            | 收盘后下载债券的行情数据。                           | 打开   |
| jobSaveEtfData_schedule             | 收盘后下载ETF的行情数据。                          | 打开   |
| jobSaveFutureData_schedule          | 收盘后下载商品期货的行情数据。                         | 打开   |
| jobSaveStockData_schedule           | 收盘后下载股票行情数据                             | 打开   |
| jobUpdateStockPools_schedule        | 最初的股票池计算方式，已废弃                          | 不打开  |
| sensorSaveStockData                 | 股票行情数据下载完成探测，探测到股票数据下载完成就开始下载指数数据下载     | 打开   |
| sensorSaveIndexData                 | 指数数据下载完成探测，探测到指数数据下载完成就开始执行计算超级赛道       | 打开   |

## 参数配置说明

系统的配置信息放在freshquant数据库的params表中

miniqmt相关配置

```json
{
  "code": "xtquant",
  "value": {
    "path": "E:\\e海方舟-量化交易版\\userdata_mini",
    "account": "2******8"
  }
}
```

| key           | value                |
| ------------- | -------------------- |
| value.path    | qmt中userdata_mini的目录 |
| value.account | qmt的账号               |

通知配置

```json
{
  "code": "notification",
  "value": {
    "webhook": {
      "dingtalk": {
        "private": "https://oapi.dingtalk.com/robot/send?access_token=******",
        "public": "https://oapi.dingtalk.com/robot/send?access_token=******"
      }
    }
  }
}
```

| key                            | value         |
| ------------------------------ | ------------- |
| value.webhook.dingtalk.private | 持仓股有信号的钉钉通知   |
| value.webhook.dingtalk.public  | 候选股票池有信号的钉钉通知 |

gardian策略配置

```json
{
  "code": "gardian",
  "value": {
    "stock": {
      "positionPct": 40,
      "autoOpen": true,
      "lot_amount": 3000,
      "singleAmount": 3000,
    }
  }
}
```

| key                      | value                                      |
| ------------------------ | ------------------------------------------ |
| value.stock.positionPct  | 持仓比例阈值，如果仓位低于这个值，那么候选股出信号的时候会自动买入。         |
| value.stock.autoOpen     | true的时候，后选股出信号的时候才会自动买入，false的时候只买卖持仓股的信号。 |
| value.stock.lot_amount   | 一次买入的最大金额，实际买入会根据行情和持仓情况低于这个值。             |
| value.stock.singleAmount | 废弃，用lot_amount替换                           |

监控程序配置

```json
{
  "code": "monitor",
  "value": {
    "stock": {
      "periods": [
        "1m"
      ]
    }
  }
}
```

| key                 | value                   |
| ------------------- | ----------------------- |
| value.stock.periods | 要监控的时间周期，数组类型，可以配置多个周期。 |

系统Dashboard的url是：http://127.0.0.1

## 在Windows上安装FQ

上面我们讲的是在Docker中安装各种服务，在windows上我们也要把FQ给安装进去，那么有些事情我们是可以在Windows上完成的，比如后面要讲的命令行运维。

我们的安装需要依赖Miniconda3，所以我们要安装好Miniconda3。用如下命令可以直接安装。

```
winget install Anaconda.Miniconda3
```

然后我们要在Miniconda3的Prompt中，创建也给给FQ用的环境，比如我们创建也给fqkit的环境。用如下的命令。

```
conda create -n fqkit python=3.10
```

到这里后，你先确保你安装了Visual Studio Community 2022。如果没有的话，先安装好，我们的C++代码需要用到他来编译。记得同时安装好Visual Studio Community 2022的C++桌面开发组件。

安装完成后，我们就可以在源码的根目录运行install.bat来来安装FQ。

当然我们要先激活这个创建的环境。

```
conda activate fqkit
```

进入到你源码存放的根目录，比如：

```
cd E:\fqkit\freshquant
```

然后运行安装脚本：

```
install.bat
```

## 番茄量化系统使用指南

### 命令行运维

系统提供了一些命令行上的运维命令，再完整的UI开发出来前，可以借助一些命令来做基本的运维。在命令行中无法运维的内容，目前只有直接去修改数据库来完成了。网页版本的运维会逐步提供，当然命令行的运维也在逐步丰富。

命令行的格式会遵循这样的格式规范：

python -m freshquant.cli <资源>[.<子资源>] <命令>  [选项]

资源分：stock, bond, etf, index, config等。

命令分：save, import, rm, set等。

子资源分：list, day, min, block等。

python -m freshquant.cli还有一种简单写法就是fqctl

即：

fqctl 等价于 python -m freshquant.cli

那么：

```
python -m freshquant.cli stock.list save
```

也可以写成：

```
fqctl stock.list save
```

选项运行命令的时候需要的其他一些选项。

#### 下载行情数据

下载股票列表

```
fqctl stock.list save
```

下载股票日线数据

```
fqctl stock.day save
```

下载股票分钟数据

```
fqctl stock.min save
```

下载股票板块数据

```
fqctl stock.block save
```

下载股票除权除息数据

```
fqctl stock.xdxr save
```

一条命令下载以上所有数据

```
fqctl stock save
```

如上的命令，就分别是下载股票列表，股票日线数据，股票分钟数据，股票板块，股票除权除息。

最后一条命令，省略子资源的情况下，就是下载所有（list, day, min, block, xdxr）的子资源。

#### 导入股票到股票池

系统中建立的三种股票池：

1. 预选股票池。存放预选的股票，比如我们之前开发的各种模型的预选结果会先存放在这里。

2. 监控股票池。从预选股票池经过人工或者自动的筛选，符合某种要求后存放到这个股票池。这个池中的股票会在盘中监控，给出买卖点提示信息。

3. 必买股票池。一般是人工直接维护，就是必须会买的股票，有买卖信号系统就直接执行交易。

为了能人工对这些股票池进行管理，提供一套命令行工具。

比如我们要给预选股票池导入数据：

```
fqctl stock.pre-pool import --file <路径> --category CLXS00001 --days 20
```

这里的文件可以是通达信的自选股文件，也就是文本文件，一行一个股票代码。category指的是导入系统后的分类，days指的是在股票池中保留多少天。

如果要导入监控股票池，只要把pre-pool改成pool就可以了。

除了指定文件，还可以直接指定股票代码。

```
fqctl stock.pre-pool import --code 000001 --category CLXS00001 --days 20
```

导入多个可以这样写：

```
fqctl stock.pre-pool import --code 000001 --code 000002 --category CLXS0001 --days 20
```

也可以这样写：

```
fqctl stock.pre-pool import --code 000001,000002 --category CLXS0001 --days 20
```

#### 查看股票池当前股票

命令格式是

查看预选股票池

```
fqctl stock.pre-pool list [--category <分类>]
```

查看监控股票池

```
fqctl stock.pool list [--category <分类>]
```

查看必买股票池

```
fqctl stock.must-pool list [--category <分类>]
```

如果后面跟上--category选项就是按分类查看，比如：

```
fqctl stock.pool list --category CLXS00001
```

#### 从股票池中删除股票

按id删除

```
fqctl stock.pool rm --id 67af2ae6628d0c02c85a9a6f
```

按category删除

```
fqctl stock.pool rm --category 超级赛道
```

按代码删除，这样都是支持的。

```
fqctl stock.pool rm --code 603103
fqctl stock.pool rm --code 603103 --code 600633
fqctl stock.pool rm --code 603103,600633
```

按category和code的组合删除

```
fqctl stock.pre-pool rm --category CLXS00001 --code 000001
```

监控股票池同理，pre-pool替换成pool。

#### 必买股票池的管理

必买股票池和预选股票池的管理有些不同，主要是多一些额外的参数，比如止损价，初始买入金额，一网买入金额。

添加的命令的格式是

```
fqctl stock.must-pool import --code <股票代码> --category <分类> --stop-loss-price <止损价> --initial-lot-amount <第一次买入的金额> --lot-amount <一网买入的金额>
```

从必买股票池删除股票的方法和pre-pool和pool一样，格式如下。

```
fqctl stock.must-pool rm --id <ID> --category <分类> --code <代码>
```

#### 运行选股程序

命令格式是：

```
fqctl stock screen clxs --model-opt <modelopt> --wave-opt <waveopt> --stretch-opt <stretchopt> --trend-opt <trendopt>
```

比如我们用CLXS的0001模型选股：

```
fqctl stock screen clxs --model-opt 10001
fqctl stock screen clxs --model-opt 1
```

运行后选出的股票也会直接被存入到pre-pool股票池。

#### 成交订单管理

如果已经对接了miniqmt的情况下，成交订单当然是已经自动地导入到系统了。但是如果还没有对接好miniqmt，那么怎么来利用系统来管理好持仓的成交订单呢。就通过这里的命令来完成。

一旦订单录入到系统后，就可以利用系统的能力，来帮你监控你的持仓，当出现交易信号的时候通知到你，没有自动交易的情况下，就手工来执行订单指令，成交之后再把成交单录入系统。如此，我们就可以和系统进行信息交换了。接下来就一一说明：

命令行说明中的约定：

方括号代表可选，尖括号代表占位。

查看系统中所有的成交单：

```
fqctl stock.fill list [--code <股票代码>]
```

```
fqctl stock.fill list
fqctk stock.fill list --code 000001
```

导入成交单到系统中：

```
fqctl stock.fill import buy --code <股票代码> --quantity <数量> --price <价格>
fqctl stock.fill import sell --code <股票代码> --quantity <数量> --price <价格>
```

如果发现某笔成交录入错了，也可以删除他。

按数据库的记录ID，删除一条记录：

```
fqctl stock.fill rm --id <数据库记录的ID>
```

按股票代码，删除所有这个股票的成交记录：

```
fqctl stock.fill rm --code <股票代码>
```

你的成交订单录入后，我们就可以在http://127.0.0.1这个页面上看到你的成交记录。并且在图表中看到你的持仓线。在盘中也可以对他们进行信号监控了。

## 其他配置

### 关闭wsl crash dump

当crash的时候，为了以后不要生成dump文件导致磁盘撑爆，可以做如下的设置调整。

第一步：

建一个文件C:\Users\\<用户名>\.wslconfig，文件中放如下的内容

```
[wsl2]
kernelCommandLine = sysctl.kernel.core_pattern=/dev/null
```

第二步：

进入wsl的linux。

然后在wsl的linux中，用如下命令更改/proc/sys/kernel/core_pattern的内容。

```
echo '/dev/null' | sudo tee /proc/sys/kernel/core_pattern
```

第三步：

这步修改是为了保证重启后，配置还是有效。修改/etc/sysctl.conf的内容，

在文件末尾添加：

```
kernel.core_pattern=/dev/null
```

```

```
