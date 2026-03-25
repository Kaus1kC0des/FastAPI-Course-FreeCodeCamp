"use client";
import Link from "next/link";
import {Bookmark, Heart, MessageCircle} from "lucide-react";
import {useBookmark} from "@/app/hooks/useBookmark";
import {useLike} from "@/app/hooks/useLike";

export default function PostCard({post}) {
    const {
        title,
        slug,
        author,
    } = post;

    const authorName = author?.name || "Unknown author";
    const isBookmarked = post.isBookmarked;
    const isLiked = post.isLiked;
    const likesCount = post.likesCount ?? 0;
    const {mutate: toggleBookmark} = useBookmark();
    const {mutate: toggleLike} = useLike();

    const handleBookmark = () => {
        toggleBookmark({postId: post.id, isBookmarked});
    };
    const handleLike = () => {
        toggleLike({postId: Number(post.id), isLiked});
    };

    return (
        <article
            className="rounded-xl border border-gray-200 bg-white p-4 transition-colors duration-200 hover:bg-gray-50">
            <Link href={slug || "/home"} className="block space-y-3">
                <h2 className="text-xl font-semibold leading-snug text-gray-900">{title}</h2>

                <div className="flex items-center gap-2">
                    <div
                        className="flex h-7 w-7 items-center justify-center rounded-full bg-gray-900 text-xs font-medium text-white"
                        style={author?.image ? {
                            backgroundImage: `url(${author.image})`,
                            backgroundSize: "cover",
                            backgroundPosition: "center",
                        } : undefined}
                    >
                        {!author?.image && authorName[0]}
                    </div>
                    <span className="text-sm text-gray-700">{authorName}</span>
                </div>
            </Link>

            <div className="mt-4 flex items-center justify-between border-t border-gray-200 pt-3 text-sm text-gray-600">
                <div className="flex items-center gap-5">
                    <button
                        type="button"
                        className="inline-flex items-center gap-1.5 hover:text-gray-900"
                        onClick={handleLike}
                    >
                        <Heart className={`h-4 w-4 ${isLiked ? "fill-current text-red-600" : ""}`}/>
                        {likesCount}
                    </button>
                    <button type="button" className="inline-flex items-center gap-1.5 hover:text-gray-900">
                        <MessageCircle className="h-4 w-4"/>
                        Comment
                    </button>
                </div>
                <button type="button" className="inline-flex items-center gap-1.5 hover:text-gray-900"
                        onClick={handleBookmark}>
                    <Bookmark className={`h-4 w-4 ${isBookmarked ? "fill-current text-blue-600" : ""}`}/>
                    {isBookmarked ? "Saved" : "Save"}
                </button>
            </div>
        </article>
    );
}
