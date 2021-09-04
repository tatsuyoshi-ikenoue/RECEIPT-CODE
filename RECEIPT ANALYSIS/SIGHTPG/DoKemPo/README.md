# ファイル・フォルダ構成

```
.
├── Health_Check_UP : 健診用コード
|   ├── Adaptor.py : 健診用コード（Main）
|   ├── Anonymizer.py : 匿名化コード
|   ├── COLUMNS_NAME.csv : 健診列名対応表
|   ├── DataConstruct.py : 健診用コード（Sub）
|   ├── cleanse.py : 洗浄用コード
|   ├── eGFR.py : eGFR算出コード
|   ├── insurance.py : 健診用コード
|   └── pdread.py : データ読み込みコード
|
└── Receipt : レセプト用コード
    ├── DATE_ANAL : 日付解析用コード
    |   └── Hospitalization.py : 入院日検出用コード
    ├── DIVIDE : レセプト分割用コード
    |
    └── PROCESS : ID作成用コード

```
