# ベースイメージの指定
FROM python:3.9

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# spaCyのモデルをダウンロード
RUN python -m spacy download en_core_web_sm

# アプリケーションファイルをコンテナにコピー
COPY . .

# ポートの公開（Flaskのデフォルトポート番号は5000です）
EXPOSE 5010

# アプリケーションの実行
CMD ["python", "app.py"]
