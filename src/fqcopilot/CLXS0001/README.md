## CLXS0001

![](CLXS0001.png)

1、2、3、4、6还是比较好理解。

说明一下什么是量价齐升：

底分型的最低K线是阳线，他的右边K线是阳线，右边K线的实体大小是左边K线实体大小的2倍，右边K线的成交量是左边K线成交量的2倍。那么右边这个K线就是量价齐升，我们作为信号提醒出来。

用了2天时间也只是完成了1-5的实现，目前6还没实现，留待以后更新。

另外每个信号还需要能单独出提醒，这个也是留待以后更新。

参数说明：

| 参数         | 默认值   | 说明                                                                           |
| ---------- | ----- | ---------------------------------------------------------------------------- |
| WAVEOPT    | 1560  | 笔控制参数                                                                        |
| STRETCHOPT | 0     | 线段控制参数，现在没有启用                                                                |
| TRENDOPT   | 0     | 走势控制参数，现在没有启用                                                                |
| MODELOPT   | 10001 | 模型参数，低位的四个数字表示是哪个模型，0001就是CLXS0001模型。高位的是控制参数，1表示要套粉色的走势，0就不需要套粉色的走势（条件更宽松）。 |

在python端的函数签名也做了改动，示例如下：

```
highs = stock_day_data.high.to_list()
lows = stock_day_data.low.to_list()
opens = stock_day_data.open.to_list()
closes = stock_day_data.close.to_list()
volumes = stock_day_data.volume.to_list()
length = len(highs)
model_opt = 10001
sigs: list<float> = fq_clxs(
    length, highs, lows, opens, closes, volumes, 
    wave_opt, stretch_opt, trend_opt, model_opt)
```

返回的sigs的元素值是0-6，和上面图中的信号序号是一致的。