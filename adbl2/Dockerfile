FROM node:lts-alpine

COPY adbl2/ adbl2/

ENV NEXT_PUBLIC_API_BASE_URL="http://192.168.237.233:10250"

WORKDIR adbl2

RUN npm install
EXPOSE 27019

CMD ["npm", "run", "dev"]
