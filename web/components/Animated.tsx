"use client";

import { motion } from "framer-motion";
import { twMerge } from "tailwind-merge";

type AnimationType = "fade" | "slide-up" | "slide-down" | "slide-left" | "slide-right" | "scale" | "none";

interface AnimatedProps {
  children: React.ReactNode;
  animation?: AnimationType;
  delay?: number;
  className?: string;
}

const animations = {
  fade: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
  },
  "slide-up": {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
  },
  "slide-down": {
    initial: { opacity: 0, y: -20 },
    animate: { opacity: 1, y: 0 },
  },
  "slide-left": {
    initial: { opacity: 0, x: 20 },
    animate: { opacity: 1, x: 0 },
  },
  "slide-right": {
    initial: { opacity: 0, x: -20 },
    animate: { opacity: 1, x: 0 },
  },
  scale: {
    initial: { opacity: 0, scale: 0.95 },
    animate: { opacity: 1, scale: 1 },
  },
  none: {
    initial: {},
    animate: {},
  },
};

export function Animated({
  children,
  animation = "fade",
  delay = 0,
  className,
}: AnimatedProps) {
  const { initial, animate } = animations[animation];
  
  return (
    <motion.div
      initial={{ ...initial, transition: { delay: delay * 0.1 } }}
      animate={{ ...animate, transition: { delay: delay * 0.1, duration: 0.4, ease: "easeOut" } }}
      className={twMerge(className)}
    >
      {children}
    </motion.div>
  );
}

export function FadeIn({
  children,
  delay = 0,
  className,
}: Omit<AnimatedProps, "animation">) {
  return (
    <Animated animation="fade" delay={delay} className={className}>
      {children}
    </Animated>
  );
}

export function SlideUp({
  children,
  delay = 0,
  className,
}: Omit<AnimatedProps, "animation">) {
  return (
    <Animated animation="slide-up" delay={delay} className={className}>
      {children}
    </Animated>
  );
}

export function SlideDown({
  children,
  delay = 0,
  className,
}: Omit<AnimatedProps, "animation">) {
  return (
    <Animated animation="slide-down" delay={delay} className={className}>
      {children}
    </Animated>
  );
}

export function ScaleIn({
  children,
  delay = 0,
  className,
}: Omit<AnimatedProps, "animation">) {
  return (
    <Animated animation="scale" delay={delay} className={className}>
      {children}
    </Animated>
  );
}

interface StaggerContainerProps {
  children: React.ReactNode;
  className?: string;
  delay?: number;
}

export function StaggerContainer({ children, className, delay = 0.05 }: StaggerContainerProps) {
  return (
    <motion.div
      className={twMerge(className)}
      initial="initial"
      animate="animate"
      variants={{
        animate: {
          transition: {
            staggerChildren: delay,
          },
        },
      }}
    >
      {children}
    </motion.div>
  );
}

interface StaggerItemProps {
  children: React.ReactNode;
  className?: string;
  animation?: AnimationType;
}

export function StaggerItem({ children, className, animation = "slide-up" }: StaggerItemProps) {
  const { initial, animate } = animations[animation];
  
  return (
    <motion.div
      className={twMerge(className)}
      variants={{
        initial,
        animate: { ...animate, transition: { duration: 0.4, ease: "easeOut" } },
      }}
    >
      {children}
    </motion.div>
  );
}