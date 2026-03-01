"use client";
import dynamic from "next/dynamic";
import {Button} from "@/components/ui/button";
import TagInput from "@/components/TagInput";

const Editor = dynamic(() => import("@/components/Editor"), { ssr: false })

export default function NewStory() {
    return (
        <main className="w-full max-w-3xl mx-auto px-6 py-12 flex flex-col gap-6">
            <input
                placeholder="Title"
                className="text-4xl font-bold outline-none border-b-2 border-gray-300 pb-2 placeholder-gray-400 w-full focus:border-gray-600 transition-colors"
            />
            <Editor/>
            <TagInput/>
            <Button className="w-fit">Publish</Button>
        </main>
    )
}