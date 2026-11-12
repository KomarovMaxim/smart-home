
# Первый этап: сборка React
FROM node:24-alpine AS build

WORKDIR /app

# Копируем информацию о зависимостях
COPY package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем остальные файлы
COPY . .

# Собираем React
RUN npm run build


# Второй этап: запуск сайта через Nginx
FROM nginx:stable-alpine

# Копируем готовый сайт
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
