# Receipt\DATE_ANAL
京大での入退院日の抽出コード（2019年12月10日現在）

# 開発担当者
* Tatsuyoshi Ikenoue

# 対象データ
全国土木データ

# ファイル・フォルダ構成

```
.
├── Hospitalization.py : 入退院抽出コード
├── NDBデータの落とし穴_奥村泰之_20180806.pdf : コード作成参照資料除去、誤入力の制御）
└── requirements_DATE_ANAL.txt : 動作環境セットアップ用ファイル
    
```

# インストール方法、コード動作環境
## コード種別・動作環境
* python, v3.6
## コード動作環境セットアップ
`$ pip install -r requirements_DATE_ANAL.txt`

# 使用方法
## Hospitalization.py

* SIファイルについて適応する<br>
* SIファイルの保存場所に合わせて変更する<br>
2: DIR = "D:\\DokenPo\\med\\" + str(target)<br>
173: DIR = "D:\\DokenPo\\med\\" + str(target)<br>
