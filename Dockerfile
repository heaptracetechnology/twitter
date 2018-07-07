FROM          node:alpine

RUN           npm install twitter
COPY          app.js /app.js

ENTRYPOINT   ["node", "/app.js"]
