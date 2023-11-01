#!/bin/bash

# Mecabのインストールスクリプト

# 必要なパッケージをインストール
sudo apt-get update
sudo apt-get install -y mecab libmecab-dev mecab-ipadic-utf8

# ライブラリの設定
echo "/usr/local/lib" | sudo tee -a /etc/ld.so.conf
sudo ldconfig

# サンプル辞書のインストール（お好みで）
# wget https://github.com/neologd/mecab-ipadic-neologd/archive/master.zip
# unzip master.zip
# cd mecab-ipadic-neologd-master
# ./bin/install-mecab-ipadic-neologd -n -a

# Mecabのバージョン確認
mecab --version
