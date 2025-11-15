from openai import OpenAI

KSC_API_KEY = "7334fd3e-8d22-45e2-b953-6daca13cd6bd" 

# MODEL = "kimi-k2-thinking"
MODEL = "deepseek-v3.2-exp"
# MODEL = "deepseek-v3.1"
# MODEL = "DeepSeek-V3-0324"
# MODEL = "DeepSeek-R1-0528"
# MODEL = "Kimi-K2-0905-Preview"
# MODEL = "Kimi-K2-Turbo-Preview"
# MODEL = "Kimi-K2-Ksyun"

client = OpenAI(
    api_key= KSC_API_KEY,
    base_url="https://kspmas.ksyun.com/v1/",
    #base_url="http://kspmas-internal.sdns.ksyun.com/v1/"
)

SYSTEM_PROMPT = "你是资深股票交易员, 请根据历史K线数据, 预测次日股票价格。"
USER_PROMPT = """
## 任务
请根据 HK.0700 最近 60天 真实 日K线数据, 预测 下一个交易日的 最低价，最高价。
严格按照 json 格式输出结果，无需再添加其他内容。
```json
{"high_price": , "low_price": }
```

## 指标说明
| 字段名 | 数据类型 | 说明 |
|--------|----------|------|
| code | str | 股票代码 |
| name | str | 股票名称 |
| time_key | str | 时间 |
| open | float | 开盘价 |
| close | float | 收盘价 |
| high | float | 最高价 |
| low | float | 最低价 |
| volume | int | 成交量 |
| turnover | float | 成交额 |
| pe_ratio | float | 市盈率 |
| turnover_rate | float | 换手率 |
| last_close | float | 昨收价 |

## 最近真实 日K线 数据
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-08-15 00:00:00","open":587.0,"close":592.0,"high":596.5,"low":584.5,"volume":22176876,"turnover":13122452831.0,"pe_ratio":25.904,"turnover_rate":0.00242,"last_close":590.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-08-18 00:00:00","open":594.0,"close":587.0,"high":596.0,"low":587.0,"volume":17590658,"turnover":10403063174.0,"pe_ratio":25.687,"turnover_rate":0.00192,"last_close":592.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-08-19 00:00:00","open":588.0,"close":592.5,"high":597.0,"low":583.0,"volume":16359474,"turnover":9665673921.0,"pe_ratio":25.928,"turnover_rate":0.00178,"last_close":587.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-08-20 00:00:00","open":589.0,"close":590.5,"high":594.5,"low":585.5,"volume":15952765,"turnover":9407128004.0,"pe_ratio":25.841,"turnover_rate":0.00174,"last_close":592.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-08-21 00:00:00","open":590.5,"close":593.0,"high":597.0,"low":589.5,"volume":14290178,"turnover":8479961596.0,"pe_ratio":25.95,"turnover_rate":0.00156,"last_close":590.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-08-22 00:00:00","open":599.0,"close":600.0,"high":606.5,"low":595.5,"volume":19378950,"turnover":11636897211.0,"pe_ratio":26.257,"turnover_rate":0.00211,"last_close":593.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-08-25 00:00:00","open":608.5,"close":614.5,"high":621.0,"low":608.0,"volume":25694519,"turnover":15801902006.0,"pe_ratio":26.892,"turnover_rate":0.0028,"last_close":600.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-08-26 00:00:00","open":612.0,"close":609.5,"high":618.0,"low":609.5,"volume":20656474,"turnover":12655282002.0,"pe_ratio":26.675,"turnover_rate":0.00225,"last_close":614.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-08-27 00:00:00","open":613.0,"close":599.0,"high":614.5,"low":595.0,"volume":21263402,"turnover":12841741312.0,"pe_ratio":26.215,"turnover_rate":0.00232,"last_close":609.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-08-28 00:00:00","open":595.0,"close":594.0,"high":599.0,"low":590.0,"volume":21712370,"turnover":12897917091.0,"pe_ratio":25.996,"turnover_rate":0.00237,"last_close":599.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-08-29 00:00:00","open":595.5,"close":596.5,"high":605.0,"low":594.0,"volume":18234935,"turnover":10915508651.0,"pe_ratio":26.106,"turnover_rate":0.00199,"last_close":594.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-01 00:00:00","open":605.0,"close":605.0,"high":610.0,"low":601.5,"volume":15958837,"turnover":9659266534.0,"pe_ratio":26.479,"turnover_rate":0.00174,"last_close":596.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-02 00:00:00","open":605.5,"close":600.5,"high":608.5,"low":599.0,"volume":14808157,"turnover":8931988423.0,"pe_ratio":26.282,"turnover_rate":0.00161,"last_close":605.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-03 00:00:00","open":606.5,"close":598.5,"high":613.0,"low":596.0,"volume":15523985,"turnover":9342307314.0,"pe_ratio":26.194,"turnover_rate":0.00169,"last_close":600.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-04 00:00:00","open":605.0,"close":592.5,"high":605.0,"low":591.0,"volume":18003934,"turnover":10709235662.0,"pe_ratio":25.933,"turnover_rate":0.00196,"last_close":598.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-05 00:00:00","open":599.5,"close":605.5,"high":609.0,"low":595.5,"volume":19047729,"turnover":11491491838.0,"pe_ratio":26.502,"turnover_rate":0.00208,"last_close":592.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-08 00:00:00","open":605.5,"close":617.5,"high":619.0,"low":605.0,"volume":21815489,"turnover":13369898978.0,"pe_ratio":27.027,"turnover_rate":0.00238,"last_close":605.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-09 00:00:00","open":620.0,"close":627.0,"high":628.0,"low":617.5,"volume":19871460,"turnover":12402857764.0,"pe_ratio":27.447,"turnover_rate":0.00217,"last_close":617.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-10 00:00:00","open":630.0,"close":633.5,"high":639.0,"low":628.0,"volume":19193376,"turnover":12190312543.0,"pe_ratio":27.732,"turnover_rate":0.00209,"last_close":627.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-11 00:00:00","open":633.0,"close":629.5,"high":633.0,"low":624.0,"volume":18191860,"turnover":11453335654.0,"pe_ratio":27.557,"turnover_rate":0.00198,"last_close":633.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-12 00:00:00","open":645.0,"close":643.5,"high":649.0,"low":642.0,"volume":20780375,"turnover":13422728502.0,"pe_ratio":28.128,"turnover_rate":0.00227,"last_close":629.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-15 00:00:00","open":646.0,"close":643.5,"high":648.5,"low":637.5,"volume":16371242,"turnover":10535685021.0,"pe_ratio":28.128,"turnover_rate":0.00179,"last_close":643.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-16 00:00:00","open":647.0,"close":645.0,"high":649.5,"low":640.5,"volume":13339685,"turnover":8609542624.0,"pe_ratio":28.199,"turnover_rate":0.00146,"last_close":643.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-17 00:00:00","open":646.5,"close":661.5,"high":663.5,"low":645.0,"volume":22349048,"turnover":14682542772.0,"pe_ratio":28.92,"turnover_rate":0.00244,"last_close":645.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-18 00:00:00","open":662.0,"close":642.0,"high":664.5,"low":635.5,"volume":29989898,"turnover":19432788713.0,"pe_ratio":28.068,"turnover_rate":0.00327,"last_close":661.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-19 00:00:00","open":647.0,"close":642.5,"high":647.0,"low":638.0,"volume":20805608,"turnover":13371042984.0,"pe_ratio":28.089,"turnover_rate":0.00227,"last_close":642.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-22 00:00:00","open":642.0,"close":641.0,"high":643.5,"low":634.0,"volume":12899662,"turnover":8240895170.0,"pe_ratio":28.024,"turnover_rate":0.00141,"last_close":642.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-23 00:00:00","open":641.5,"close":635.5,"high":643.5,"low":627.0,"volume":15293080,"turnover":9697688016.0,"pe_ratio":27.783,"turnover_rate":0.00167,"last_close":641.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-24 00:00:00","open":633.5,"close":648.5,"high":651.0,"low":628.0,"volume":18440788,"turnover":11854753855.0,"pe_ratio":28.352,"turnover_rate":0.00201,"last_close":635.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-25 00:00:00","open":651.0,"close":650.0,"high":659.0,"low":643.5,"volume":17384258,"turnover":11337641855.0,"pe_ratio":28.417,"turnover_rate":0.0019,"last_close":648.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-26 00:00:00","open":645.0,"close":644.0,"high":653.0,"low":640.0,"volume":19504951,"turnover":12617897920.0,"pe_ratio":28.156,"turnover_rate":0.00213,"last_close":650.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-29 00:00:00","open":649.5,"close":660.0,"high":664.5,"low":647.5,"volume":20489556,"turnover":13492727746.0,"pe_ratio":28.857,"turnover_rate":0.00224,"last_close":644.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-09-30 00:00:00","open":658.0,"close":663.0,"high":666.5,"low":657.5,"volume":20610633,"turnover":13653530623.0,"pe_ratio":28.955,"turnover_rate":0.00225,"last_close":660.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-02 00:00:00","open":667.5,"close":676.5,"high":683.0,"low":665.5,"volume":17137745,"turnover":11602077362.0,"pe_ratio":29.545,"turnover_rate":0.00187,"last_close":663.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-03 00:00:00","open":677.0,"close":673.5,"high":680.0,"low":670.0,"volume":7125093,"turnover":4802401785.0,"pe_ratio":29.414,"turnover_rate":0.00078,"last_close":676.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-06 00:00:00","open":675.0,"close":677.5,"high":682.5,"low":670.0,"volume":7828323,"turnover":5290177514.0,"pe_ratio":29.589,"turnover_rate":0.00086,"last_close":673.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-08 00:00:00","open":680.0,"close":675.0,"high":680.0,"low":669.5,"volume":10540730,"turnover":7110636784.0,"pe_ratio":29.479,"turnover_rate":0.00115,"last_close":677.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-09 00:00:00","open":675.0,"close":675.5,"high":681.0,"low":665.5,"volume":14454705,"turnover":9752967437.0,"pe_ratio":29.504,"turnover_rate":0.00158,"last_close":675.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-10 00:00:00","open":669.0,"close":651.5,"high":669.0,"low":647.5,"volume":19904705,"turnover":13051085790.0,"pe_ratio":28.455,"turnover_rate":0.00217,"last_close":675.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-13 00:00:00","open":630.0,"close":639.0,"high":648.5,"low":622.5,"volume":38012175,"turnover":24133784941.0,"pe_ratio":27.91,"turnover_rate":0.00415,"last_close":651.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-14 00:00:00","open":642.5,"close":621.0,"high":644.0,"low":617.0,"volume":26797863,"turnover":16792282108.0,"pe_ratio":27.123,"turnover_rate":0.00293,"last_close":639.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-15 00:00:00","open":624.5,"close":627.0,"high":633.0,"low":620.5,"volume":18381023,"turnover":11538283646.0,"pe_ratio":27.385,"turnover_rate":0.00201,"last_close":621.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-16 00:00:00","open":626.0,"close":620.0,"high":629.0,"low":615.5,"volume":14285465,"turnover":8878516698.0,"pe_ratio":27.08,"turnover_rate":0.00156,"last_close":627.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-17 00:00:00","open":618.5,"close":608.0,"high":620.5,"low":602.5,"volume":18654519,"turnover":11370789563.0,"pe_ratio":26.556,"turnover_rate":0.00204,"last_close":620.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-20 00:00:00","open":624.0,"close":627.5,"high":632.5,"low":621.5,"volume":14963360,"turnover":9379379881.0,"pe_ratio":27.407,"turnover_rate":0.00163,"last_close":608.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-21 00:00:00","open":643.0,"close":630.5,"high":644.0,"low":630.0,"volume":14171988,"turnover":9028696332.0,"pe_ratio":27.538,"turnover_rate":0.00155,"last_close":627.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-22 00:00:00","open":626.0,"close":623.5,"high":629.0,"low":616.5,"volume":9979448,"turnover":6212763895.0,"pe_ratio":27.233,"turnover_rate":0.00109,"last_close":630.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-23 00:00:00","open":620.0,"close":633.0,"high":636.0,"low":618.0,"volume":12419348,"turnover":7782734766.0,"pe_ratio":27.647,"turnover_rate":0.00136,"last_close":623.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-24 00:00:00","open":639.0,"close":637.5,"high":641.5,"low":633.5,"volume":11997034,"turnover":7648872118.0,"pe_ratio":27.844,"turnover_rate":0.00131,"last_close":633.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-27 00:00:00","open":649.0,"close":656.0,"high":656.0,"low":646.0,"volume":16043970,"turnover":10461683006.0,"pe_ratio":28.652,"turnover_rate":0.00175,"last_close":637.5}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-28 00:00:00","open":656.0,"close":645.0,"high":656.0,"low":641.0,"volume":16295470,"turnover":10562802667.0,"pe_ratio":28.172,"turnover_rate":0.00178,"last_close":656.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-30 00:00:00","open":657.0,"close":651.0,"high":664.0,"low":645.0,"volume":21772780,"turnover":14256261211.0,"pe_ratio":28.434,"turnover_rate":0.00238,"last_close":645.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-10-31 00:00:00","open":651.5,"close":629.0,"high":655.0,"low":629.0,"volume":20578283,"turnover":13087941470.0,"pe_ratio":27.473,"turnover_rate":0.00225,"last_close":651.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-11-03 00:00:00","open":630.5,"close":628.0,"high":634.0,"low":622.5,"volume":11591004,"turnover":7277219053.0,"pe_ratio":27.429,"turnover_rate":0.00127,"last_close":629.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-11-04 00:00:00","open":631.0,"close":629.0,"high":640.0,"low":625.5,"volume":14972125,"turnover":9460748363.0,"pe_ratio":27.473,"turnover_rate":0.00164,"last_close":628.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-11-05 00:00:00","open":621.0,"close":629.0,"high":632.0,"low":613.0,"volume":13309811,"turnover":8309972605.0,"pe_ratio":27.473,"turnover_rate":0.00145,"last_close":629.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-11-06 00:00:00","open":629.5,"close":644.0,"high":645.5,"low":629.5,"volume":13081287,"turnover":8382246994.0,"pe_ratio":28.128,"turnover_rate":0.00143,"last_close":629.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-11-07 00:00:00","open":638.0,"close":634.0,"high":643.0,"low":628.5,"volume":13314360,"turnover":8434344187.0,"pe_ratio":27.665,"turnover_rate":0.00146,"last_close":644.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-11-10 00:00:00","open":641.0,"close":649.5,"high":651.0,"low":641.0,"volume":14513815,"turnover":9386838459.0,"pe_ratio":28.341,"turnover_rate":0.00159,"last_close":634.0}
{"code":"HK.00700","name":"腾讯控股","time_key":"2025-11-11 00:00:00","open":662.0,"close":650.0,"high":662.0,"low":641.0,"volume":13087772,"turnover":8483781693.0,"pe_ratio":28.363,"turnover_rate":0.00143,"last_close":649.5}
"""

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
    model= MODEL,  # your model endpoint ID
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT },
        {"role": "user", "content": USER_PROMPT },
    ],
    temperature = 0.1,
    max_tokens = 16384,
    top_p = 0.95,
    extra_body={"chat_template_kwargs": {"thinking": False}}
)

print("----- Response. -----")
#print(completion.choices[0].message)
print(completion.choices[0].message.content)

print("----- Reasoning. -----")
print(completion.choices[0].message.reasoning_content)
