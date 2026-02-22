import Link from "next/link";
import {Button} from "@/components/ui/button";

export default function Home() {
    return (
        <main className="min-h-screen bg-gray-50 bg-contain bg-center"
              style={{backgroundImage: "url('/images/home-page-background.jpg"}}>
            <section className="max-w-5xl mx-auto px-6 py-20 text-center">
                <h1 className="text-5xl font-bold mb-6">
                    FastAPI + Next.js
                </h1>

                <p className="text-lg text-gray-600 mb-8">
                    Clean frontend. Solid backend. Modern stack.
                </p>

                <Button className="bg-sky-600 hover:bg-black lg:px-8 lg:py-8 ">
                    <Link href="/login">
                        Get Started
                    </Link>
                </Button>
            </section>
        </main>
    );
}
