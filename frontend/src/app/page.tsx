import BentoGrid from "@/components/BentoGrid";
import Header from "@/components/Header";
import ContainerSection from "@/components/section/Container";

export default function Home() {
  return (
    <div className="mx-auto flex min-h-screen max-w-screen-lg flex-col items-center px-5">
      <Header />
      <BentoGrid>
        <ContainerSection />
      </BentoGrid>
    </div>
  );
}
