"use client";
import React, { useState } from "react";
import { HoveredLink, Menu, MenuItem, ProductItem } from "../components/ui/navbar-menu";
import { cn } from "@/lib/utils";

export function NavbarDemo() {
  return (
    <div className="relative w-full flex items-center bg-blue-800 justify-center">
      <Navbar className="top-2" />
      <p className="text-black dark:text-white">
        The Navbar will show on top of the page
      </p>
    </div>
  );
}

function Navbar({ className }: { className?: string }) {
  const [active, setActive] = useState<string | null>(null);

  const handleMenuItemClick = (item: string) => {
    setActive(item);
    
    if (item === "CHAT") {
      <HoveredLink href="/hobby">Hobby</HoveredLink>
    }
  };

  return (
    <div
      className={cn("fixed top-10 inset-x-0 max-w-2xl mx-auto z-50 font-bold text-white", className)}
    >
      <Menu setActive={setActive}>
        {/* <MenuItem setActive={() => handleMenuItemClick("HOME")} active={active} item="HOME" />
        <MenuItem setActive={() => handleMenuItemClick("CHAT")} active={active} item="CHAT" />
        <MenuItem setActive={() => handleMenuItemClick("MY CHATS")} active={active} item="MY CHATS" />
        <MenuItem setActive={() => handleMenuItemClick("BLOG")} active={active} item="BLOG" />
        <MenuItem setActive={() => handleMenuItemClick("CONTACT")} active={active} item="CONTACT" /> */}
        <HoveredLink href="/">HOME</HoveredLink>
        <HoveredLink href="/chat">CHAT</HoveredLink>
        <HoveredLink href="/mychat">MY CHATS</HoveredLink>
        <HoveredLink href="/blog">BLOG</HoveredLink>
        <HoveredLink href="/contact">CONTACT</HoveredLink>
        <MenuItem setActive={() => handleMenuItemClick("PROFILE")} active={active} item="PROFILE">
          <div className="flex flex-col space-y-4 text-sm">
            <HoveredLink href="/hobby">Hobby</HoveredLink>
            <HoveredLink href="/individual">Individual</HoveredLink>
            <HoveredLink href="/team">Team</HoveredLink>
            <HoveredLink href="/enterprise">Enterprise</HoveredLink>
          </div>
        </MenuItem>
      </Menu>
    </div>
  );
}
