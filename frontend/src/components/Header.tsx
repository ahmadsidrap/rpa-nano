"use client";

import Link from "next/link";
import Logo from "./Logo";
import { buttonVariants } from "./ui/button";
import { cn } from "@/lib/utils";
import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

interface NavItem {
  href: string;
  title: string;
  target?: string;
}

const navItems: NavItem[] = [];

export default function Header() {
  const [isOpen, setIsOpen] = useState(false);
  return (
    <header className="w-full py-6">
      <div className="flex w-full items-center justify-between">
        <Link href={"/"} className="flex items-center gap-2">
          <Logo />
          <div className="flex w-4/5 flex-col gap-1 uppercase lg:w-auto">
            <h1 className="text-sm leading-none md:text-xl">RPA Nano</h1>
            <span className="text-[8px] lg:text-sm">
              Nano services for your RPA needs
            </span>
          </div>
        </Link>
        <nav className="flex justify-end gap-2 text-sm md:gap-10 md:text-lg">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="feather feather-menu cursor-pointer md:hidden"
            onClick={() => setIsOpen(!isOpen)}
          >
            {/* Top Line */}
            <line
              x1="3"
              y1="6"
              x2="21"
              y2="6"
              className={cn(
                "origin-left transition-transform duration-300",
                isOpen && "-translate-y-1 rotate-45",
              )}
            />
            {/* Middle Line */}
            <line
              x1="3"
              y1="12"
              x2="21"
              y2="12"
              className={cn(
                "transition-opacity duration-300",
                isOpen && "opacity-0",
              )}
            />
            {/* Bottom Line */}
            <line
              x1="3"
              y1="18"
              x2="21"
              y2="18"
              className={cn(
                "origin-left transition-transform duration-300",
                isOpen && "translate-y-1 -rotate-45",
              )}
            />
          </svg>
          {navItems.map((nav, i) => (
            <Link
              key={i}
              href={nav.href}
              aria-label={nav.title}
              className="nav-item hidden md:inline-flex"
              target={nav.target}
            >
              {nav.title}
            </Link>
          ))}
          <Link
            href={"#"}
            className={cn(
              buttonVariants({ variant: "default" }),
              "hidden md:inline-flex",
            )}
          >
            Sign In
          </Link>
        </nav>
      </div>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0 }}
            animate={{ height: "auto" }}
            exit={{ height: 0 }}
            className="overflow-hidden"
          >
            <div className="flex h-auto w-full flex-col items-center gap-5 py-4">
              {navItems.map((nav, i) => (
                <Link
                  key={i}
                  href={nav.href}
                  aria-label={nav.title}
                  className="nav-item md:hidden"
                  target={nav.target}
                >
                  {nav.title}
                </Link>
              ))}
              <Link
                href={"#"}
                className={cn(
                  buttonVariants({ variant: "default" }),
                  "md:hidden",
                )}
              >
                Sign In
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
