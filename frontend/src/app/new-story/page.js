"use client";
import Editor from "@/components/Editor";
import {Button} from "@/components/ui/button";

export default function NewStory() {
    return (
        <main className="max-w-3xl mx-auto px-6 py-12 flex flex-col gap-6">
            <input
                placeholder="Title"
                className="text-4xl font-bold outline-none border-none placeholder-gray-300 w-full"
            />
            <hr className="border-gray-200"/>
            <Editor/>
            <Button className="w-fit">Publish</Button>
        </main>
    )
}