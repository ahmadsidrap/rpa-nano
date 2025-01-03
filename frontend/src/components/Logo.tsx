import Image from "next/image";

export default function Logo() {
  return (
    <div className="relative aspect-square h-10 w-10 rounded-full md:h-14 md:w-14">
      <Image
        src={"/logo.jpg"}
        alt="Kerja IT Jepang"
        fill
        className="rounded-full object-cover"
      />
    </div>
  );
}
