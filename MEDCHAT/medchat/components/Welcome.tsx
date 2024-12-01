"use client";
import { motion } from "framer-motion";
import React from "react";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { ButtonsCard } from "./ui/tailwindcss-buttons";
import { useRouter } from "next/navigation";

export function Welcome() {

  const router = useRouter();

  const handleButton = () => {
    router.push("/find-symptom")
  }

  return (
    <AuroraBackground>
      <motion.div
        initial={{ opacity: 0.0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{
          delay: 0.3,
          duration: 0.8,
          ease: "easeInOut",
        }}
        className="relative flex flex-col gap-4 items-center justify-center px-4"
      >
        <div className="text-3xl md:text-7xl font-bold dark:text-white text-center">
          MEDCHAT
        </div>
        <div className="font-extralight text-base md:text-4xl dark:text-neutral-200 py-4">
          CHeck your symptom today ! 
        </div>
        {/* <button className="bg-blue-800 dark:bg-white rounded-full w-fit text-white dark:text-black px-4 py-2">
          TRY NOW
        </button> */}

<button className="inline-flex h-12 animate-shimmer items-center justify-center rounded-md border border-slate-800 bg-[linear-gradient(110deg,#0e7490,45%,#164e63,55%,#083344)] bg-[length:200%_100%] px-6 font-medium text-slate-400 transition-colors focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50" onClick={handleButton}>
        TRY NOW
      </button>

      </motion.div>
    </AuroraBackground>
  );
}

export const buttons = [
  {
    name: "Shimmer",
    description: "Shimmer button for your website",
    // showDot: false,
    // component: (
    //   <button className="inline-flex h-12 animate-shimmer items-center justify-center rounded-md border border-slate-800 bg-[linear-gradient(110deg,#0e7490,45%,#164e63,55%,#083344)] bg-[length:200%_100%] px-6 font-medium text-slate-400 transition-colors focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50" onClick={handleButton}>
    //     TRY NOW
    //   </button>
    // ),
    code: `
        // Button code
        <button className="inline-flex h-12 animate-shimmer items-center justify-center rounded-md border border-slate-800 bg-[linear-gradient(110deg,#000103,45%,#1e2631,55%,#000103)] bg-[length:200%_100%] px-6 font-medium text-slate-400 transition-colors focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-50">
          Shimmer
        </button>
  
        // tailwind.config.js code
        {
          "animation": {
            shimmer: "shimmer 2s linear infinite"
          },
          "keyframes": {
            shimmer: {
              from: {
                "backgroundPosition": "0 0"
              },
              to: {
                "backgroundPosition": "-200% 0"
              }
            }
          }
        }
      `,
  }
]