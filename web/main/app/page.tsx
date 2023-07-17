import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <main>
      <div
        className="min-h-screen hero"
        style={{
          backgroundImage: "url(./shiueo_wallpaper_v4.png)",
        }}
      >
        <div className="bg-opacity-50 hero-overlay"></div>
        <div className="text-center hero-content text-neutral-content">
          <div className="max-w-5xl">
            <h1 className="mb-5 text-3xl font-bold">
              활기찬 가상세계 Natzhashite의 시민이 되어보시는 건 어떤가요?
            </h1>
            <p className="mb-5">
              Natzhashite의 심장부! 대도시 Schtarn에서 만나요!
            </p>
            <Link href="https://discord.gg/NXwVfdcygM" className="btn">
              가자!
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
