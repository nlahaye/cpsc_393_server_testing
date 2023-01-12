ARG USER
FROM nvcr.io/nvidia/tensorflow:22.12-tf2-py3

USER 0

WORKDIR /app

RUN wget https://github.com/sagar448/Keras-Convolutional-Neural-Network-Python/archive/refs/heads/master.zip && \
unzip master.zip && cd Keras-Convolutional-Neural-Network-Python-master/ && sed -i 's/keras/tensorflow.keras/g' 'Convolutional Neural Network for Object Recognition.py' && \
sed -i 's/np_utils as u/to_categorical/g' 'Convolutional Neural Network for Object Recognition.py' && sed -i 's/u\.//g' 'Convolutional Neural Network for Object Recognition.py' && \
sed -i 's/\.convolutional//g' 'Convolutional Neural Network for Object Recognition.py' && sed -i 's/&2.f%%" %/\", str/g' 'Convolutional Neural Network for Object Recognition.py'

COPY run_test.sh /app

run chmod -R a+rwx /app

ENTRYPOINT ["/app/run_test.sh"]

