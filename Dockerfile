# This Dockerfile is not needed for Railway deployment
# Railway supports Next.js natively without Docker
# Use this file only if you want to deploy with Docker on other platforms

FROM node:18-alpine

WORKDIR /app

RUN apk add --no-cache libc6-compat

COPY package*.json ./
RUN npm ci

COPY . .

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

EXPOSE 3000
ENV PORT=3000

CMD ["npm", "start"]
