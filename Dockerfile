ARG USER
FROM nvcr.io/nvidia/tensorflow:21.05-tf2-py3

USER 0

WORKDIR /app

RUN wget https://github.com/sagar448/Keras-Convolutional-Neural-Network-Python/archive/refs/heads/master.zip && \
unzip master.zip && cd Keras-Convolutional-Neural-Network-Python-master/ && sed -i 's/keras/tensorflow.keras/g' 'Convolutional Neural Network for Object Recognition.py' && \
sed -i 's/np_utils as u/to_categorical/g' 'Convolutional Neural Network for Object Recognition.py' && sed -i 's/u\.//g' 'Convolutional Neural Network for Object Recognition.py' && \
sed -i 's/\.convolutional//g' 'Convolutional Neural Network for Object Recognition.py' && \
sed -i 's/&2.f%%" %/\", str/g' 'Convolutional Neural Network for Object Recognition.py' && \
sed -i 's/import cifar10/import cifar10\nfrom tensorflow.compat.v1.keras import backend as K\nimport tensorflow as tf\nconfig = tf.compat.v1.ConfigProto( device_count = {\"GPU\": 1 , \"CPU\": 15} )\nsess = tf.compat.v1.Session(config=config)\nK.set_session(sess)/' 'Convolutional Neural Network for Object Recognition.py'

COPY run_test.sh /app

run chmod -R a+rwx /app

ENTRYPOINT ["/app/run_test.sh"]

