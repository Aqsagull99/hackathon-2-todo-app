# syntax=docker/dockerfile:1

# === Build stage: Install dependencies and build Next.js application ===
FROM node:20-alpine AS builder

# Define build arguments to be used as environment variables during build
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ARG NEXT_PUBLIC_CHAT_API_URL=http://localhost:8000/api/chat
ARG BETTER_AUTH_URL=http://localhost:3000
ARG BETTER_AUTH_SECRET=temp-secret-for-build
ARG DATABASE_URL=postgresql://user:password@localhost:5432/todoapp

# Set environment variables for the build process
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_CHAT_API_URL=$NEXT_PUBLIC_CHAT_API_URL
ENV BETTER_AUTH_URL=$BETTER_AUTH_URL
ENV BETTER_AUTH_SECRET=$BETTER_AUTH_SECRET
ENV DATABASE_URL=$DATABASE_URL

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build the Next.js app
RUN npm run build

# === Production stage: Create minimal runtime image ===
FROM node:20-alpine AS runner

WORKDIR /app

# Install dumb-init for signal processing and zombie reaping
RUN apk add --no-cache dumb-init

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

# Copy built application from builder stage
COPY --from=builder --chown=nextjs:nodejs /app ./

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000 || exit 1

# Start the application with dumb-init
ENTRYPOINT ["dumb-init", "--"]
CMD ["npm", "start"]