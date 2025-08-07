# CuraGenie Frontend Dockerfile - Optimized for Railway/Vercel
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies
RUN apk add --no-cache libc6-compat

# Copy package files
COPY package*.json ./

# Install all dependencies (including devDependencies for build)
RUN npm install

# Copy source code
COPY . .

# Set environment variables
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Set port environment variable
ENV PORT=3000

# Start the application
CMD ["npm", "start"]
