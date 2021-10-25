# python:3.8の公式 image をベースの image として設定
FROM python:3.8

# 作業ディレクトリの作成
RUN mkdir /stokee_proj

# 作業ディレクトリの設定
WORKDIR /stokee_proj

# カレントディレクトリにあるプログラムをコンテナ上の指定のディレクトリにコピーする
ADD ./stokee_proj /stokee_proj

# 言語設定
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

# エディタを入れる（ほかのでもOk）
RUN apt-get update
RUN apt-get install -y vim 

# pipセットアップ
RUN pip install --upgrade pip

# 本当はrequirements.txtを作るべきだと思うけれど、、、
RUN pip install Django==2.2.1
RUN pip install django-mathfilters
RUN pip install django-bootstrap4
RUN pip install numpy
RUN pip install pandas
RUN pip install scikit-learn
RUN pip install -r requirements.txt


# ポートオープン参考 https://hub.docker.com/_/django
EXPOSE 8000 