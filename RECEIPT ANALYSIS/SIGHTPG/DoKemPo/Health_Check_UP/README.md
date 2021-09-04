# Health_Check_UP
京大でのレセプト分割用のコード（2019年12月10日現在）

# 開発担当者
* Tatsuyoshi Ikenoue

# 対象データ
全国土木健診データ

# ファイル・フォルダ構成

```
.
├── Adaptor.py : 健診用コード（Main）
├── Anonymizer.py : 匿名化コード
├── COLUMNS_NAME.csv : 健診列名対応表
├── DataConstruct.py : 健診用コード（Sub）
├── cleanse.py : 洗浄用コード
├── eGFR.py : eGFR算出コード
├── insurance.py : ID付与コード
├── requirements_Health_Check_UP.txt
└── pdread.py : データ読み込みコード
    
```

# インストール方法、コード動作環境
## コード種別・動作環境
* python, v3.6
## コード動作環境セットアップ
`$ pip install -r requirements_Health_Check_UP.txt`

# 使用方法
## Adaptor.py
* 効能<br>
> * レセプト共通IDの付与<br>
> * データのクリーニング(HbA1cの統一、尿検査の数値化など)<br>
> * eGFRの追加（日本腎臓学会の式およびCKD_EPIの式）<br>

* 特定健診の置いてあるDIRを指定<br>
DIR = "*D:\土木健保データ原本写し\特定健診*"<br>

## Anonymizer.py
* 効能<br>
> * 名前の匿名化<br>

* 対象ファイルを指定<br>
9: df = csv(r"*D:\土木健保データ原本写し\特定健診\H30_Specific_Health_Checkups.csv*").headder()<br>

## COLUMNS_NAME.csv
* 土健保の健診データは年度ごとにフォーマットが異なるのでこのファイルでフォーマットを合わせる

## DataConstruct.py

## その他のコードは上記.py内で使用



