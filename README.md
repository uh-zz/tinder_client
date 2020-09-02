tinder_client
====

## Description
- tinderでひたすらいいねし続けるだけのアプリ

## Requirement
- git

## Usage

以下、パッケージをインストール
(後々Dockerに移行するのでそれまでローカルで動かしたい場合)

```
pip install selenium
pip install chromedriver-binary==Chromeバージョン番号
```
Chromeバージョンは、ブラウザのURLに`chrome://version/`を入力して「Google Chrome」のバージョン番号を入力する。


tinder_client.py:10行目
'--user-data-dir=(プロフィールパス)'

プロフィールパスは、ブラウザのURLに`chrome://version/`を入力して「プロフィールパス」の「Default」を除いた残りのパスを入力する。


## Author

[NakZMichael](https://github.com/NakZMichael)
[uh-zz](https://github.com/uh-zz)
