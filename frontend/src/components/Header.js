import {
    SignInButton,
    SignUpButton,
    SignedIn,
    SignedOut,
    UserButton,
} from '@clerk/nextjs';
import {Button} from "@/components/ui/button";
import {Fragment} from "react";
import Link from "next/link"
import {SquarePen} from "lucide-react"


export default function Header() {
    return (
        <Fragment>
            <header className="flex justify-between items-center p-4 gap-4 h-19 align-middle border-b border-black">
                <div
                    className="ml-[15%] header-brandname text-3xl font-bold"
                    style={{
                        fontFamily: "Fixedsys62, sohne, 'Helvetica Neue', Arial, sans-serif",
                        letterSpacing: "-0.05em",
                        fontSize: "1.75em"
                    }}
                >
                    TECHNOLOOGIA
                </div>
                <div className="flex gap-4 items-center mr-[15%]">
                    <SignedOut>
                        <SignInButton mode="redirect" forceRedirectUrl="/home"/>
                        <SignUpButton mode="redirect" forceRedirectUrl="/home">
                            <button
                                className="bg-[#6c47ff] text-white rounded-full font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 cursor-pointer">
                                Sign Up
                            </button>
                        </SignUpButton>
                    </SignedOut>

                    <SignedIn afterSignInUrl="/home">
                        <Link href="/new-story">
                            <Button className="new-story" variant="outline">
                                <SquarePen className="ml-1.5"/>
                                <p className="overflow-hidden">New Story</p>
                            </Button>
                        </Link>
                        <UserButton/>
                    </SignedIn>
                </div>
            </header>
        </Fragment>
    )
}