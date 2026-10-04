# ==============================================================================
# Next.js 15 Production Multi-Stage Dockerfile (`src/frontend/Dockerfile`)
# Multi-Agent Dev Team — Antigravity 2.0
# Output: Standalone (~110MB ultra-lightweight image)
# ==============================================================================

# Stage 1: Install production and build dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Install libc6-compat for Alpine compatibility with SWC / Turbopack
RUN apk add --no-cache libc6-compat

COPY package.json package-lock.json ./
RUN npm ci

# Stage 2: Build Next.js application in standalone mode
FROM node:20-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Environment variables for build time
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

RUN npm run build

# Stage 3: Production runner image
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Security: Run as dedicated non-root user (OWASP compliance)
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Ensure public folder exists and copy it
RUN mkdir -p ./public
COPY --from=builder /app/public ./public 2>/dev/null || true

# Copy Next.js standalone server and static assets
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

# Periodic healthcheck
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:3000/ || exit 1

CMD ["node", "server.js"]
