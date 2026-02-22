"use client";

import {SignIn, SignUp} from "@clerk/nextjs";
import {Tabs, TabsList, TabsTrigger} from "@/components/ui/tabs";
import {useState} from "react";

export default function LoginPage() {
    const [isSignIn, setIsSignIn] = useState(true);
    return (
        <main className="min-h-screen flex items-center justify-center bg-gray-600 px-4">
            {/* Container matches Clerk component width (400px) */}
            <div className="w-[400px] max-w-full space-y-6">
                {/* Tabs inherit container width */}
                <Tabs defaultValue="signin" className="w-full"
                      onValueChange={(value) => setIsSignIn(value === "signin")}>
                    <TabsList className="grid w-full grid-cols-2 bg-gray-200 rounded-lg p-1">
                        <TabsTrigger
                            value="signin"
                            className="rounded-md data-[state=active]:bg-white data-[state=active]:shadow-none"
                        >
                            Sign In
                        </TabsTrigger>
                        <TabsTrigger
                            value="signup"
                            className="rounded-md data-[state=active]:bg-white data-[state=active]:shadow-none"
                        >
                            Sign Up
                        </TabsTrigger>
                    </TabsList>
                </Tabs>

                {/* Fixed min-height prevents layout shift when switching */}
                <div className="flex justify-center min-h-[600px]">
                    {isSignIn ? <SignIn routing="hash"/> : <SignUp routing="hash"/>}
                </div>
            </div>
        </main>
    );
}
