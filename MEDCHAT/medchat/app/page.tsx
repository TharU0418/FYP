import { Footer } from "@/components/Footer";
import HowItWork from "@/components/HowItWork";
import { NavbarDemo } from "@/components/NavbarDemo"
import { Welcome } from "@/components/Welcome";
import { WhatIsTHis } from "@/components/WhatIsThis";

export default function Home() {
  return (
    <div>
      {/* <NavbarDemo/> */}
      <div className="relative">
        <Welcome/>
      </div>
      <WhatIsTHis/>
      <HowItWork/>

      <div className="relative">
      {/* <Footer/> */}

      </div>

    </div>
  );
}
