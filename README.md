# 智慧建築系統整合 × BA 軟體開發

我是智慧建築系統整合工程師，也寫 BA。現場遇到設備資料難接、點位難查、弱電規劃反覆修改、案場進度分散時，我會把處理方法做成自己和同事能使用的工具。

**求職方向：**智慧建築／BA 系統整合、BMS 解決方案、樓宇自動化應用開發，以及需要工程現場經驗與軟體能力的職務。

## 先看四個代表作品

| 作品 | 現場問題 | 我做出的解法 |
|---|---|---|
| [BA Gateway 與戰情看板](case-studies/ba-gateway.md) | 設備有回應卻沒有正確數值，現場難判斷卡在連線、協定還是點位 | 將設備接入、點位驗證、採集狀態、警報與看板整合成一套流程 |
| [弱電視覺化規劃器](case-studies/low-voltage-planner.md) | 設備清單、Port、PoE 和上聯分散在多張表，修改後容易對不上 | 在畫面分配設備並即時檢查工程規則，再產生規劃表 |
| [導覽機內容管理與網頁播放器](case-studies/kiosk-studio.md) | 螢幕內容、版型與播放設備需要反覆更新，工程人員逐台修改不易維護 | 將頁面編輯、素材、發布版本與螢幕指派串成管理流程 |
| [弱電案場進度管制系統](case-studies/project-tracker.md) | 多人改 Excel、卡關原因分散、週報要重新整理 | 以 Web 系統管理案場、工作項目、附件、異動和週報 |

### BA Gateway：從設備資料到現場看板

![BA Gateway 示範看板，含即時狀態與趨勢](images/ba-demo-dashboard.jpg)

看板使用系統內建的示範資料。[看點位列表、看板管理、編輯器與兩種播放畫面](case-studies/ba-gateway.md)

### 弱電規劃：在畫面上看清 Port 與上聯

![弱電規劃器顯示交換器、Port 和樓層上聯](images/planner-topology-test.png)

[看設備分配、PoE 檢查與表格輸出](case-studies/low-voltage-planner.md)

### 導覽機：讓內容更新與螢幕播放可管理

![導覽機內容管理首頁](images/kiosk-dashboard-demo.png)

從管理介面處理頁面、素材、發布版本與播放設備；畫面採展示資料。[看管理首頁、統計頁與資訊元件](case-studies/kiosk-studio.md)

### 案場管理：進度、卡關與週報在同一套系統

![弱電案場進度系統的總覽畫面](images/tracker-dashboard-demo.png)

這張畫面由原系統使用虛構案場資料拍攝。[看完整操作畫面：清單、詳情、工作項目、週報與 LOG](case-studies/project-tracker.md)

## 其他我做的工具

我也寫了電錶與水錶分析、Modbus 模擬、離線偵測、工程表格整理、告警通知、數位看板、圖片處理等工具。[查看全部 24 個工具與開發試驗](TOOLS_CATALOG.md)。

其中幾個可深入閱讀：

- [能源與用水分析](case-studies/energy-water-analytics.md)：處理累積讀值、重置與日統計。
- [設備離線偵測](case-studies/device-health-monitor.md)：用連續成功／失敗門檻避免狀態抖動。
- [Modbus 訊號模擬器](case-studies/modbus-simulator.md)：設備未到場前先測點位與畫面。
- [工程文件自動整理](case-studies/engineering-doc-automation.md)：從文件與規劃資料產生點位、接線和審查表。
- [系統可靠度統計](case-studies/reliability-statistics.md)：依系統整理警報與異常紀錄。
- [數位看板編輯與播放](case-studies/digital-signage.md)：以瀏覽器編排多媒體頁面，附原系統編輯器畫面。

## 可以實際試的程式

- [BA 底圖批次最佳化工具](public-code/ba-image-optimizer/README.md)：選資料夾、設定格式與品質、批次輸出，保留原圖。
- [通用 Modbus 暫存器解碼示範](public-code/modbus-register-decoder/README.md)：用虛構暫存器測試比例、位元、浮點數與字組順序。

大型系統的完整程式與現場設定沒有放在此倉庫；這裡提供作品介紹、操作畫面與可安全執行的示範程式。
