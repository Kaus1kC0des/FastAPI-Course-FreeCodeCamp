"use client";

import {useState} from "react";
import {Plus} from "lucide-react";
import {Button} from "@/components/ui/button";

export default function TagInput() {
    const [isOpen, setIsOpen] = useState(false);
    const [tags, setTags] = useState([]);
    const [inputValue, setInputValue] = useState([]);

    const handleKeyDown = (e) => {
        if (e.key === "Enter" || e.key === ",") {
            e.preventDefault();
            const tag = inputValue.trim().replace(/^#/, "");
            if (tag && !tags.includes(tag)) {
                setTags([...tags, tag]);
            }
            setInputValue("");
        }
    }

    return (
        <div>
            {!isOpen && (
                <Button onClick={() => setIsOpen(!isOpen)} variant="outline" className="mb-2">
                    <Plus/> Add Tags
                </Button>
            )}
            {isOpen && (
                <div className="flex flex-wrap gap-2 border rounded-md p-2">
                    {tags.map(tag => (
                        <span key={tag} className="bg-gray-100 px-2 py-1 rounded-full text-sm flex items-center gap-1">
                            #{tag}
                            <button onClick={() => setTags(tags.filter(t => t !== tag))} className="text-gray-400 hover:text-black">×</button>
                        </span>
                    ))}
                    <input
                        autoFocus
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Add a tag"
                        className="outline-none text-sm"
                    />
                </div>
            )}
        </div>
    )
}