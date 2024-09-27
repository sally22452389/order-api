# 資料庫測驗
## 題目一
2023 年 5 月下訂的訂單, 使用台幣付款且5月總金額最
多的前 10 筆的旅宿 ID (bnb_id), 旅宿名稱 (bnb_name), 5 月總金額 (may_amount)
```sql
SELECT orders.bnb_id, bnbs.name, SUM(orders.amount) AS may_amount
FROM orders INNER JOIN bnbs ON orders.bnb_id = bnbs.id
WHERE orders.currency = 'TWD' AND orders.created_at >= '2023-05-01' AND orders.created_at < '2023-06-01'
GROUP BY orders.bnb_id, bnbs.name
ORDER BY may_amount DESC
LIMIT 10;
```

## 題目二
SQL 執行速度優化方式
### 1.建立索引
常用的過濾與關聯欄位 bnb_id, created_at, currency 建立索引加快查詢速度
```sql
CREATE INDEX idx_orders_currency_created_at ON orders (currency, created_at);
CREATE INDEX idx_orders_bnb_id ON orders (bnb_id);
```

### 2.RANGE Partitioning
MySQL 可以使用 RANGE 分區來提升查詢效率，p_may 表示 2023 年 5 月的資料
```sql
PARTITION BY RANGE (TO_DAYS(created_at)) (
  PARTITION p_before_may VALUES LESS THAN (TO_DAYS('2023-05-01')),
  PARTITION p_may VALUES LESS THAN (TO_DAYS('2023-06-01')),
  PARTITION p_after_may VALUES LESS THAN MAXVALUE
);
```

# 專案中使用到的 SOLID

## 單一職責原則
`Order_validator` 僅負責驗證訂單的必要欄位和是否為指定型別 
`checking` 僅負責檢查訂單格式
`currency_transformer` 僅負責貨幣轉換

## 開放封閉原則
如果需要增加新的檢查規則，可以繼承或擴展 `checking` 不需要修改現有的程式碼
`currency_transformer` `transform` 貨幣轉換，不需修改現有方式，也可以擴展其他更有效的轉換方式

## 里氏替換原則
如果建立新的 `other_checking` 子類別，實作其他檢查邏輯，但依然可以替換原本的 `checking` 類別

## 介面隔離原則
`order_controller` 中 `create_order` 沒有依賴多餘或不必要的方法

## 依賴反轉原則
高階模組不依賴於低階模組: `OrderService` 不依賴於實作 `Checking`, `CurrencyTransformer` 
抽象不依賴於實作: 抽象 `interfaces` 不依賴於實作
實作依賴於抽象: `Checking`, `CurrencyTransformer` 依賴於抽象

# 專案中用到的設計模式

## 工廠方法模式 (Factory Method Pattern)
收到 data 做成 `order` 物件及物件轉換成 json

## 外觀模式 (Facade Pattern)
`order_service` 整理了訂單格式檢查、貨幣轉換等功能，是容易使用和理解的

## 範本方法模式 (TemplateMethod Pattern)
`checking` 定義檢查流程，再由子類別完成