FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
FROM node:20-alpine AS build
WORKDIR /client
COPY client/package*.json ./
RUN npm ci
COPY client/ .
RUN sed -i 's|http://localhost:5050||g' src/components/*.jsx
RUN npm run build

FROM node:20-alpine
WORKDIR /app
ENV PORT=5000
COPY server/package*.json ./
RUN npm ci --omit=dev
COPY server/ .
COPY --from=build /client/dist ./public
EXPOSE 5000
CMD ["node", "server.js"]
