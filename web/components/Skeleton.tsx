"use client";

import { motion } from "framer-motion";

interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={`animate-pulse bg-gradient-to-r from-muted via-muted/50 to-muted bg-[length:200%_100%] ${className}`}
      style={{
        backgroundImage: "linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.05) 50%, transparent 100%)",
        backgroundSize: "200% 100%",
        animation: "shimmer 1.5s ease-in-out infinite",
      }}
    />
  );
}

export function MessageSkeleton() {
  return (
    <div className="flex gap-4">
      <div className="w-8 h-8 rounded-full overflow-hidden flex-shrink-0">
        <Skeleton className="w-full h-full rounded-full" />
      </div>
      <div className="flex-1 space-y-3">
        <Skeleton className="h-4 w-32 rounded" />
        <div className="space-y-2">
          <Skeleton className="h-4 w-full rounded" />
          <Skeleton className="h-4 w-4/5 rounded" />
          <Skeleton className="h-4 w-3/5 rounded" />
        </div>
      </div>
    </div>
  );
}

export function ChatListSkeleton() {
  return (
    <div className="space-y-2 p-2">
      {[1, 2, 3].map((i) => (
        <div key={i} className="p-3 rounded-lg bg-muted/30">
          <Skeleton className="h-4 w-3/4 rounded mb-2" />
          <Skeleton className="h-3 w-1/3 rounded" />
        </div>
      ))}
    </div>
  );
}

export function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex gap-1 items-center"
    >
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          animate={{ y: [0, -5, 0] }}
          transition={{
            duration: 0.6,
            repeat: Infinity,
            delay: i * 0.15,
          }}
          className="w-2 h-2 bg-primary rounded-full"
        />
      ))}
    </motion.div>
  );
}