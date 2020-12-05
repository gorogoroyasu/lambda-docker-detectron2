ARG FUNCTION_DIR="/function/"

FROM python:3.8.6

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  libopencv-dev && \
  apt-get autoremove -y

RUN pip install torch torchvision opencv-python boto3
RUN pip install 'git+https://github.com/facebookresearch/detectron2.git'
RUN mkdir -p ${FUNCTION_DIR}
COPY app/* ${FUNCTION_DIR}
# モデルのダウンロードを毎回していたら重いので、Docker Image にしておく。
COPY model_final_721ade.pkl /root/.torch/fvcore_cache/detectron2/COCO-Detection/faster_rcnn_R_50_C4_1x/137257644/model_final_721ade.pkl
RUN pip install \
    --target ${FUNCTION_DIR} \
        awslambdaric

WORKDIR ${FUNCTION_DIR}
# Copy in the built dependencies
# COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD [ "app.handler" ]