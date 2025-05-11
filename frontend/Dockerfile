# frontend/Dockerfile

# Stage 1: Build the Next.js application
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

# Install dependencies
# If you're using yarn, replace with: COPY yarn.lock ./ \ && yarn install --frozen-lockfile
RUN npm install

# Copy the rest of the application code
COPY . .

# Set environment variables for the build phase if needed
# ARG NEXT_PUBLIC_API_BASE_URL
# ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}

# Build the Next.js application
# If you have specific build arguments for NEXT_PUBLIC_API_BASE_URL, they should be passed here too
RUN npm run build

# Stage 2: Serve the built application using a lightweight server
FROM node:18-alpine

WORKDIR /app

# Copy only the necessary artifacts from the builder stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
# If you have a custom server, copy that too. For standalone output, this might not be needed.
# COPY --from=builder /app/next.config.mjs ./next.config.mjs # If you are using standalone output, this may not be needed

# Expose the port Next.js runs on (default 3000)
EXPOSE 3000

# Set environment variables for the run phase
# This is where you'd set NEXT_PUBLIC_API_BASE_URL if it's needed at runtime and not just build time
# ENV NODE_ENV production
# ENV NEXT_PUBLIC_API_BASE_URL http://backend:8000/api/v1 # Example, assuming backend is reachable as 'backend'

# Start the Next.js application
# The default command for Next.js production server
CMD ["npm", "start"]
