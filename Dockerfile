FROM          node:alpine

RUN           npm install twitter lodash
COPY          app.js /app.js

ENTRYPOINT   ["node", "/app.js"]
