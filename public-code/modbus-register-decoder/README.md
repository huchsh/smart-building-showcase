# 通用 Modbus 暫存器解析示範

從 BA 解析工具中的訊號解碼邏輯抽出、重寫的精簡範例。使用虛構暫存器資料，**不連接實體設備**，也不包含廠牌 Profile、案場 IP 或控制命令。

支援 16 位元有號／無號值、位元旗標、32 位元浮點與整數、四種常見字組順序、比例與有效範圍檢查。

## 為什麼要做

工程師拿到設備的暫存器表時，還要判斷數值型態、位元位置、Endian 和比例。只要其中一項錯，畫面可能顯示錯值。這個小範例把解析規則寫成資料設定，讓同一段讀值可重複測試。

## 用虛構資料試一次

在本資料夾開啟 Python，執行：

```python
from decoder import decode_signal

temperature = decode_signal([253], {"type": "UINT", "scale": 0.1})
running = decode_signal([8], {"type": "BOOL", "bit": 3})
print(temperature, running)
```

輸出為 `25.3 1.0`。前者是比例換算，後者從第 3 個 bit 取出狀態。[查看三種資料型態的示範結果](../../images/modbus-decoder-demo.png)。

## 驗證

```powershell
python -m unittest discover -s . -p "test_*.py"
```

完整系統的設備連線、設定與寫入控制程式不在此公開範例中。
