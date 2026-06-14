FROM node:20-alpine

WORKDIR /app/frontend

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy all frontend files
COPY . .

# Build Next.js app
RUN npm run build

EXPOSE 3000

# Start production server
CMD ["npm", "start"]
