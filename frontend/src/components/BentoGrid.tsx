export default function BentoGrid({ children }: { children: React.ReactNode }) {
  return (
    <main className="my-6 flex w-full items-center justify-center lg:my-10">
      <div className="grid w-full auto-rows-min grid-cols-12 gap-6">
        {children}
      </div>
    </main>
  );
}
