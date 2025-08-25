# frontend/Dockerfile
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy all frontend files
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Run dev server
CMD ["npm", "run", "dev"]
