# ---------- Build stage ----------
FROM node:20 AS build

WORKDIR /app

# Copy package files (already inside frontend/)
COPY package.json package-lock.json ./

RUN npm install

# Copy rest of frontend code
COPY . .

RUN npm run build

# ---------- Runtime stage ----------
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
