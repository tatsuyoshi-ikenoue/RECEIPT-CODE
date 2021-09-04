# PROCESS:ID CREATION
京大でのID作成用のコード（2019年12月10日現在）

# 開発担当者
* Tatsuyoshi Ikenoue

# 対象データ
全国土木分割データ（レセプト種別ごとに分割）

# ファイル・フォルダ構成

```
.
├── ID.py : IDを付与する
├── ImportData.py : データを読み込んで各ファイルにIDを付与する（メイン）
├── generateID.py : IDを作成する
├── requirements_IDCreation.txt : 動作環境セットアップ用ファイル
└── sample : サンプルデータ
    ├── prescriptions_data_med.ho.csv : hoデータ
    ├── prescriptions_data_med.ir.csv : irデータ
    └── rescriptions_data_med.re.csv : reデータ

```

# インストール方法、コード動作環境
## コード種別・動作環境
* python, v3.6
## コード動作環境セットアップ
`$ pip install -r requirements_IDCreation.txt`

