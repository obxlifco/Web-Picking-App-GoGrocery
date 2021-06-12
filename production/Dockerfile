FROM node:"11.6.0" as builder
RUN mkdir  -p /home/lifco
RUN mkdir /home/lifco/production
WORKDIR /home/lifco/production
ADD . /home/lifco/production
ADD package.json /home/lifco/production
#ADD protractor.conf.js /home/lifco/production
ADD angular.json /home/lifco/production
#ADD karma.conf.js /home/lifco/production
RUN npm cache clean --force
RUN npm -g config set user root
#RUN npm set progress=false

#RUN rm -rf node_modules
#RUN npm install -global typescript@3.2.4
RUN npm install -g @angular/cli@7.3.2
RUN npm install

#RUN npm list -g --depth=0
#RUN npm i -g npm-check-updates
#RUN npm-check-updates -u
#RUN npm install

#RUN ng build --aot=false
#RUN ng build --prod --build-optimizer --max_old_space_size=4192
RUN node --max_old_space_size=4192 node_modules/@angular/cli/bin/ng build --prod --build-optimizer

#RUN ls -al
#RUN ng serve --host=192.168.0.205 --port=4200
FROM nginx:latest
COPY conf.d/nginx.conf /etc/nginx/nginx.conf
RUN rm -rf /usr/share/nginx/html
COPY src/ /usr/share/nginx/html
RUN ls -al
COPY --from=builder /home/lifco/production/dist/ /usr/share/nginx/html
COPY --from=builder /home/lifco/production/src /usr/share/nginx/html/src
WORKDIR /usr/share/nginx/html
RUN ls -al

#EXPOSE 8083

CMD ["nginx", "-g", "daemon off;"]
#EXPOSE 4200
# Serve the app

#CMD ["npm", "start"]