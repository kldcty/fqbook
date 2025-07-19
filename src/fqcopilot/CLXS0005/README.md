## CLXS0005

此模型是一个二买模型，第一次预警是在c点，这是一个二买提醒点，第二次预警是在e点，这是一个类二买提醒点。

![](CLXS0005-1.png)

当MODELOPT==00005的时候，b点和d的要求只要比ZD高，不要求比ZG高，如上图。

![](CLXS0005-2.png)

当MODELOPT==10005的时候，b点和d的要求比ZG高，如上图。

另外你还可以控制只需要c点或者e点，或者两者都要。看下选股代码中的最后2句：

```
RESET:=TDXDLL7(1,0,0,0);
IG1:=TDXDLL7(2, 6, WAVEOPT, 0);
IG2:=TDXDLL7(2, 7, STRETCHOPT, 0);
IG3:=TDXDLL7(2, 8, TRENDOPT, 0);
IG4:=TDXDLL7(2, 9, MODELOPT, 0);
IG5:=TDXDLL7(2, 3, OPEN, 0);
IG6:=TDXDLL7(2, 5, VOL, 0);
SIG:=TDXDLL7(3,HIGH,LOW,CLOSE);
BUY_OPEN:SIG>0;
```

当SIG>0的时候，c点和e点两个都要。

当SIG>100 AND SIG<200的时候，只要c点。

当SIG>200的时候，只要e点。