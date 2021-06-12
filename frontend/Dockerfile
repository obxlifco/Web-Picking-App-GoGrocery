FROM node:10-alpine as buildContainer
RUN mkdir  -p /home/lifco
RUN mkdir /home/lifco/frontend
WORKDIR /home/lifco/frontend
COPY ./package.json /home/lifco/frontend
COPY ./angular.json /home/lifco/frontend
RUN npm config set unsafe-perm true
RUN npm cache clean --force
RUN npm -g config set user root
RUN npm install
RUN npm install --save angularx-social-login@2.2.1
COPY . /home/lifco/frontend
RUN npm run build:prod
#RUN npm run serve:ssr
#RUN npm run test:ssr

FROM node:8-alpine

WORKDIR /home/lifco/frontend
# Copy dependency definitions
COPY --from=buildContainer /home/lifco/frontend/package.json /home/lifco/frontend
COPY --from=buildContainer /home/lifco/frontend/local.js /home/lifco/frontend
COPY --from=buildContainer /home/lifco/frontend/src/.well-known/apple-app-site-association /home/lifco/frontend
COPY --from=buildContainer /home/lifco/frontend/conf.d/ssl/www_gogrocery_ae.crt /home/lifco/frontend/conf.d/ssl/www_gogrocery_ae.crt
COPY --from=buildContainer /home/lifco/frontend/conf.d/ssl/www_gogrocery_ae.key /home/lifco/frontend/conf.d/ssl/www_gogrocery_ae.key

# Get all the code needed to run the app
COPY --from=buildContainer /home/lifco/frontend/dist /home/lifco/frontend/dist



# Expose the port the app runs in
# Expose the port the app runs in
EXPOSE 82


# Serve the app

CMD ["node", "/home/lifco/frontend/local"]
#CMD ["node", "/home/lifco/frontend/dist/server"]

