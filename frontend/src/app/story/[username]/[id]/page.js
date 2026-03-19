"use client";

import {useParams} from "next/navigation";
import {AlertMessage} from "@/components/AlertMessage";
import {Skeleton} from "@/components/ui/skeleton";
import {Bookmark, Heart, MessageCircle} from "lucide-react";
import {usePost} from "@/app/hooks/usePost";
import {useBookmark} from "@/app/hooks/useBookmark";

function toDisplayDate(isoDate) {
    if (!isoDate) return "Unknown date";
    return new Date(isoDate).toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric",
    });
}

function toReadingTime(html) {
    const plainText = (html || "").replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
    const words = plainText ? plainText.split(" ").length : 0;
    return `${Math.max(1, Math.ceil(words / 200))} min read`;
}

export default function StoryPage() {
    const {id, username} = useParams();
    const {data: story, isLoading, isError, error: queryError} = usePost(id);
    const {mutate: toggleBookmark} = useBookmark();

    const handleBookmark = () => {
        if (story) {
            toggleBookmark({postId: story.id, isBookmarked: story.isBookmarked});
        }
    };

    if (isLoading) {
        return (
            <main className="mx-auto w-full max-w-3xl px-6 py-12 space-y-6">
                <Skeleton className="h-12 w-3/4"/>
                <Skeleton className="h-6 w-1/2"/>
                <Skeleton className="h-5 w-full"/>
                <Skeleton className="h-5 w-full"/>
                <Skeleton className="h-5 w-11/12"/>
            </main>
        );
    }

    if (isError) {
        return (
            <main className="mx-auto w-full max-w-3xl px-6 py-12">
                <AlertMessage 
                    title="Failed to load story" 
                    message={queryError?.response?.data?.detail || queryError?.message || "Could not fetch this story."}
                />
            </main>
        );
    }

    if (!story) {
        return (
            <main className="mx-auto w-full max-w-3xl px-6 py-12">
                <p className="text-sm text-gray-500">Story not found.</p>
            </main>
        );
    }

    const authorName = [story.author?.first_name, story.author?.last_name]
        .filter(Boolean)
        .join(" ")
        .trim() || story.author?.username || "Unknown author";
    const displayUsername = story.author?.username || username || "unknown";

    return (
        <main className="mx-auto w-full max-w-3xl px-6 py-12">
            <article className="space-y-8">
                <header className="space-y-5">
                    <h1 className="text-4xl font-bold leading-tight text-gray-900 md:text-5xl">{story.title}</h1>
                    <div className="flex flex-wrap items-center gap-3 text-sm text-gray-600">
                        <div className="flex items-center gap-2">
                            <div
                                className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-900 text-sm font-semibold text-white"
                                style={story.author?.image ? {
                                    backgroundImage: `url(${story.author.image})`,
                                    backgroundSize: "cover",
                                    backgroundPosition: "center",
                                } : undefined}
                            >
                                {!story.author?.image && authorName[0]}
                            </div>
                            <div className="flex flex-col">
                                <span className="font-medium text-gray-900">{authorName}</span>
                                <span className="text-xs text-gray-500">
                                    @{displayUsername} • {story.author?.role || "Author"}
                                </span>
                            </div>
                        </div>
                        <span>•</span>
                        <span>{toDisplayDate(story.created_at)}</span>
                        <span>•</span>
                        <span>{toReadingTime(story.content)}</span>
                    </div>
                    {story.tags?.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                            {story.tags.map((tag) => (
                                <span
                                    key={tag.id}
                                    className="rounded-full bg-gray-100 px-3 py-1 text-xs text-gray-700"
                                >
                                    #{tag.tag}
                                </span>
                            ))}
                        </div>
                    )}

                    <div
                        className="flex items-center justify-between border-y border-gray-200 py-3 text-sm text-gray-600">
                        <div className="flex items-center gap-6">
                            <button type="button" className="inline-flex items-center gap-1.5 hover:text-gray-900">
                                <Heart className="h-4 w-4"/>
                                Like
                            </button>
                            <button type="button" className="inline-flex items-center gap-1.5 hover:text-gray-900">
                                <MessageCircle className="h-4 w-4"/>
                                Comment
                            </button>
                        </div>
                        <button 
                            type="button" 
                            className="inline-flex items-center gap-1.5 hover:text-gray-900"
                            onClick={handleBookmark}
                        >
                            <Bookmark className={`h-4 w-4 ${story.isBookmarked ? "fill-current text-blue-600" : ""}`}/>
                            {story.isBookmarked ? "Saved" : "Save"}
                        </button>
                    </div>
                </header>

                <section
                    className="text-[1.1rem] leading-8 text-gray-800 [&_h1]:mt-8 [&_h1]:mb-4 [&_h1]:text-3xl [&_h1]:font-bold [&_h2]:mt-7 [&_h2]:mb-3 [&_h2]:text-2xl [&_h2]:font-semibold [&_p]:mb-5 [&_blockquote]:my-6 [&_blockquote]:border-l-4 [&_blockquote]:border-gray-300 [&_blockquote]:pl-4 [&_blockquote]:italic [&_code]:rounded [&_code]:bg-gray-100 [&_code]:px-1.5 [&_code]:py-0.5 [&_ul]:my-5 [&_ul]:list-disc [&_ul]:pl-6 [&_ol]:my-5 [&_ol]:list-decimal [&_ol]:pl-6"
                    dangerouslySetInnerHTML={{__html: story.content}}
                />
            </article>
        </main>
    );
}
