import Link from "next/link";
import {Button} from "@/components/ui/button";

export default function Home() {
    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-start">
            <section className="max-w-5xl px-4 md:px-6 text-left ml-4 md:ml-[15%] mr-4">
                <h1 className="text-4xl md:text-7xl font-normal mb-4 md:mb-6 tracking-tight"
                    style={{
                        fontFamily: "sohne, 'Helvetica Neue', Arial, sans-serif",
                        letterSpacing: "-0.05em",
                    }}
                >
                    Tech Ideas, Experiences & Strategies
                </h1>

                <p className="text-lg md:text-2xl text-gray-800 mb-6 md:mb-8"
                   style={{fontFamily: "sohne, 'Helvetica Neue', Arial, sans-serif"}}
                >
                    A place to share your thoughts, feelings and ideas with the world!
                </p>

                <Button className="bg-black hover:bg-blue-500 px-6 md:px-12 py-4 md:py-6 text-base md:text-xl rounded-full">
                    <Link href="/login">
                        Let's get you talking!
                    </Link>
                </Button>
            </section>
        </div>
    );
}
