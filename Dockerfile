# ベースイメージとしてPython 3の公式イメージを使用
FROM python:3.10

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY . /app

# Pythonパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# Flaskサーバーを起動
CMD ["python", "app.py"]
