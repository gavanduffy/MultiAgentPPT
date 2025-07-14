# Dockerfile

FROM node:22-alpine

WORKDIR /app
RUN apk update
RUN apk add --no-cache openssl

COPY . .

ENV DATABASE_URL=postgresql://postgres:welcome@localhost:5432/presentation_ai
ENV A2A_AGENT_OUTLINE_URL=http://127.0.0.1:10001
ENV A2A_AGENT_SLIDES_URL=http://127.0.0.1:10012

RUN npm install -g pnpm
RUN pnpm install
# 正式环境才build
RUN pnpm build

EXPOSE 3000

CMD ["pnpm", "start"]
