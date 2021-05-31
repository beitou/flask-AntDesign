FROM harbor.xiaobangtouzi.com/base/node:alpine as npm_builder

WORKDIR /data

ADD .eslintrc.js /data/
ADD .prettierrc.js /data/
ADD ava.config.js /data/
ADD e2e.config.js /data/
ADD nuxt.config.js /data/
ADD unit.config.js /data/
ADD package.json /data/
ADD package-lock.json /data/
ADD fe /data/fe

RUN npm ci
RUN npm run generate

FROM harbor.xiaobangtouzi.com/base/python:3.7.5-alpine3.10

WORKDIR /data/quality

COPY . /data/quality

RUN echo "http://mirrors.aliyun.com/alpine/v3.10/main/" > /etc/apk/repositories \
  && apk update --no-cache \
  && apk upgrade --no-cache \
  && apk add --no-cache build-base nginx openldap-dev libffi-dev mariadb-dev tzdata jpeg-dev zlib-dev \
  && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && echo 'Asia/Shanghai' > /etc/timezone \
  && sed '/st_mysql_options options;/a unsigned int reconnect;' /usr/include/mysql/mysql.h -i.bkp \
  && pip3 --no-cache-dir install -r /data/quality/requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY --from=npm_builder /data/fe/dist/ /data/quality/dist/

CMD cat hosts >> /etc/hosts && gunicorn quality:app -c gconfig.py && nginx -c /data/quality/nginx.conf -g "daemon off;"
