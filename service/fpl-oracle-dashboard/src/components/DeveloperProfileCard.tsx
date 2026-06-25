/**
 * FILE: /src/components/DeveloperProfileCard.tsx
 * PURPOSE: Renders quick developer profiles, social connections, and FPL credentials for Naresh Koirala.
 * USAGE: Placed as a supportive profile card in the /src/App.tsx bottom rail layout or dashboard sidebar.
 */

import { Mail, Github, Globe, Linkedin } from "lucide-react";

export default function DeveloperProfileCard() {
  return (
    <div className="clay-card p-5 border-white/5 space-y-4">
      <div className="border-b border-white/5 pb-2.5">
        <span className="text-[10px] font-mono text-[#00ff85] font-black tracking-widest uppercase">Developer Profile</span>
        <h4 className="text-sm font-bold text-white mt-0.5">Naresh Koirala</h4>
      </div>
      
      <div className="space-y-2 text-xs font-mono">
        <a 
          href="mailto:koiralanaresh10@gmail.com" 
          className="flex items-center gap-2.5 text-white/50 hover:text-[#00ff85] transition duration-150 group"
        >
          <Mail className="h-4 w-4 text-white/30 group-hover:text-[#00ff85] shrink-0" />
          <span className="truncate">koiralanaresh10@gmail.com</span>
        </a>
        
        <a 
          href="https://github.com/Naresh Koirala" 
          target="_blank" 
          referrerPolicy="no-referrer"
          className="flex items-center gap-2.5 text-white/50 hover:text-[#00ff85] transition duration-150 group"
        >
          <Github className="h-4 w-4 text-white/30 group-hover:text-[#00ff85] shrink-0" />
          <span className="truncate">github.com/Naresh Koirala</span>
        </a>
        
        <a 
          href="https://nareshkoirala.dev" 
          target="_blank" 
          referrerPolicy="no-referrer"
          className="flex items-center gap-2.5 text-white/50 hover:text-[#00ff85] transition duration-150 group"
        >
          <Globe className="h-4 w-4 text-white/30 group-hover:text-[#00ff85] shrink-0" />
          <span className="truncate">nareshkoirala.dev</span>
        </a>
        
        <a 
          href="https://linkedin.com/in/naresh-koirala" 
          target="_blank" 
          referrerPolicy="no-referrer"
          className="flex items-center gap-2.5 text-white/50 hover:text-[#00ff85] transition duration-150 group"
        >
          <Linkedin className="h-4 w-4 text-white/30 group-hover:text-[#00ff85] shrink-0" />
          <span className="truncate">linkedin.com/in/naresh-koirala</span>
        </a>
      </div>
    </div>
  );
}
