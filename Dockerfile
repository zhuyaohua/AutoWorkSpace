#基础镜像为python运行环境，版本为3.8,
FROM python:3.8

#设置环境变量
ENV PATH /usr/local/bin:$PATH
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python run.py