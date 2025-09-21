# Fqlite指南

Fqlite项目使用uv做管理，参考uv官网了解工具的用法：https://docs.astral.sh/uv/

## Fqlite环境准备

为fqlite创建python运行环境，在fqlite的根目录下运行：

```
uv venv --python 3.12
```

新建的环境中是没有pip程序的，在这个python环境中安装pip，运行：

```
uv pip install pip
```

激活进入这个python环境，运行：

```
activate.bat
```

告诉fqlite，你的通达信的安装目录，运行。

```
set TDX_HOME=你的通达信根目录
```

安装fqlite的依赖库，运行：

```
uv sync
```

安装fqchan04和fqcopilot，python安装包在星球或者纷传上载的压缩包中，（根据你实际使用的python版本和操作系统选择）。

```
pip install fqchan04-YYYY-M-D-cp12-cp12-win_amd64.whl
pip install fqcopilot-YYYY-M-D-cp12-cp12-win_amd64.whl
```

## 运行选股

### 强底分型

```
python fqlite/screen/strong_factor.poy
```

### CLXS系列模型选股

通过--model-opt指定运行哪个模型，比如：

```
python fqlite/screen/clxs.py --model-opt 10001
python fqlite/screen/clxs.py --model-opt 1
python fqlite/screen/clxs.py --model-opt 8
python fqlite/screen/clxs.py --model-opt 9
```
