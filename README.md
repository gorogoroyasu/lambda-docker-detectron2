AWS Lambdaがコンテナイメージをサポートしたので、Detectron2 を使って画像認識(Object Detection)を行うAPI を作る

Qiita の記事の実装です。
動作検証用なので、実際にご利用いただくにはコードを直接編集して頂く必要があります。
お手数おかけしますが、ご了承くださいませ。

簡単に使い方をご紹介します。

## 事前準備

```sh
$ git clone git@github.com:gorogoroyasu/lambda-docker-detectron2.git
$ cd lambda-docker-detectron2
$ wget https://dl.fbaipublicfiles.com/detectron2/COCO-Detection/faster_rcnn_R_50_C4_1x/137257644/model_final_721ade.pkl
```


## sh build_and_run.sh
このコマンドで、イメージをビルドして、実行します。
ローカルでは、S3 へのアクセス権限が与えられていないので、適宜付与するか、demo.from_s3_to_tmp を書き換えて、問題が起きないように修正してください。

## curl または access.py
このコマンドで、ローカルでの動作確認ができます。

```sh
$ curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"bucket": "YOUR_BUCKET_NAME", "s3_path": "path/to/jpg"}'
```

もしくは、access.py の `is_local = True` の状態で動かすと、local での動作検証ができます。
access.py の `is_local = False ` を設定すると、AWS を叩きに行きます。
Lambda Function Name 等は、適宜設定してください。
