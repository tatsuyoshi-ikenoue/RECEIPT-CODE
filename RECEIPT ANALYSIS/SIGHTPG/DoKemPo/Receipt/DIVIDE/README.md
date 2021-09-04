# Receipt\DIVIDE
京大でのレセプト分割用のコード（2019年12月10日現在）

# 開発担当者
* Tatsuyoshi Ikenoue

# 対象データ
全国土木データ

# ファイル・フォルダ構成

```
.
├── 1_MODIFIED_Assign receipt number to Dokenpo Receipt_DPC.py : DPC分割用コード
├── 1_MODIFIED_Assign receipt number to Dokenpo Receipt_MED.py : MED分割用コード
├── 1_MODIFIED_Assign receipt number to Dokenpo Receipt_PHA.py : PHA分割用コード
├── 2_HO_reproduct_20190720.py : HOファイルのクリーニング（重複の除去、誤入力の制御）
├── requirements_DIVIDE.txt : 動作環境セットアップ用ファイル
└── pdread : 読み込み用パッケージ
    
```

# インストール方法、コード動作環境
## コード種別・動作環境
* python, v3.6
## コード動作環境セットアップ
`$ pip install -r requirements_DIVIDE.txt`

# 使用方法
## 1_MODIFIED_Assign receipt number to Dokenpo Receipt_DPC.py
## 1_MODIFIED_Assign receipt number to Dokenpo Receipt_MED.py
## 1_MODIFIED_Assign receipt number to Dokenpo Receipt_PHA.py

* DIRの部分を原本の入っているフォルダに変更する<br>
14: DIR = r"*D:\土木健保データ原本写し\20191105\提供データ\診療報酬明細書*"<br>
* DIRの部分を保存先のフォルダに変更する<br>
296: DIR = r'*D:\DokenPo*'<br>


## 2_HO_reproduct_20190720.py
* ターゲットとするレセプトの種類を設定する<br>
6: Target = *'pha'*<br>
> * DPC -> 'dpc'<br>
> * 医科 -> 'med'<br>
> * 調剤 -> 'pha'<br>

* "1_MODIFIED_Assign receipt number to Dokenpo Receipt"で設定した保存先に変更する<br>
32: DIR = os.path.join(*"D:\DokenPo"*, str(Target))<br>

