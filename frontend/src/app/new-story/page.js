"use client";
import dynamic from "next/dynamic";
import {Button} from "@/components/ui/button";
import {AlertMessage} from "@/components/AlertMessage";
import TagInput from "@/components/TagInput";
import {api} from "@/lib/api";
import {useState, useRef} from "react";
import {useAuth} from "@clerk/nextjs";

const Editor = dynamic(() => import("@/components/Editor"), {ssr: false})

export default function NewStory() {
    const editorRef = useRef(null);
    const [tags, setTags] = useState([]);
    const [error, setError] = useState(null);
    const [content, setContent] = useState("");
    const [title, setTitle] = useState("");
    const {getToken} = useAuth();

    async function handlePublish() {
        const token = await getToken();
        if (!title.trim()) {
            setError({
                title: "Title empty",
                message: "Title of a post can't be empty. What do you call a nameless creature...?"
            });
            setTimeout(() => setError(null), 1000);
            return;
        }
        const isContentEmpty = !editorRef.current ||
            editorRef.current.document.every(block => block.content.length === 0);
        if (isContentEmpty) {
            setError({
                title: "Content Empty",
                message: "Empty article is something users can't read right? Let's fill it with something you think...."
            });

            setTimeout(() => setError(null), 1000);
            return;
        }
        await api.post("/posts",
            {title, content, tags},
            {
                headers: {Authorization: `Bearer ${token}`}
            }
        );
    }

    return (
        <main className="w-full max-w-3xl mx-auto px-6 py-12 flex flex-col gap-6">
            <input
                placeholder="Title"
                className="text-4xl font-bold outline-none border-b-2 border-gray-300 pb-2 placeholder-gray-400 w-full focus:border-gray-600 transition-colors"
                onChange={(e) => setTitle(e.target.value)}
            />
            <Editor setContent={setContent} onEditorReady={(e) => editorRef.current = e}/>
            <TagInput tags={tags} setTags={setTags}/>
            {error && <AlertMessage title={error.title} message={error.message}/>}
            <Button className="w-fit" onClick={handlePublish}>Publish</Button>
        </main>
    )
}