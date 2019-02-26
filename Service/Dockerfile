FROM  gcr.io/howathon-attrition-predictor/attrition:latest

WORKDIR /home/howathon/

#RUN apt-get update \
#  && apt-get install -y python3-pip python3-dev \
#  && cd /usr/local/bin \
#  && ln -s /usr/bin/python3 python \
#  && pip3 install --upgrade pip

COPY . /home/howathon/

RUN apt-get update -y
RUN apt-get install sudo -y
#RUN apt-get install -y emacs
#RUN apt-get install -y wget bzip2
RUN apt-get upgrade -y 
RUN apt-get install curl -y
RUN apt-get install vim -y
#RUN sudo apt-get install --reinstall coreutils
RUN sudo apt-get install nginx -y
RUN chmod a+rwx /home/howathon/
RUN sudo -H pip3 install --upgrade pip
RUN pip install -r requirements.txt


RUN rm /etc/nginx/nginx.conf

COPY nginx.conf /etc/nginx/


RUN sudo nginx -t
RUN sudo service nginx restart

EXPOSE 5000
EXPOSE 8000

CMD ["sh", "/home/howathon/services.sh"]