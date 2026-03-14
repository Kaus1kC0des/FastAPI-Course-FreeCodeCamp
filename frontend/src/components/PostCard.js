import Link from "next/link";
import {CalendarDays, Clock3, Hash} from "lucide-react";
import {Separator} from "@/components/ui/separator";

export default function PostCard({post}) {
    const {
        title,
        excerpt,
        slug,
        publishedAt,
        readingTime,
        tags = [],
        author,
    } = post;
    const authorName = author?.name || "Unknown author";

    return (
        <article className="rounded-xl border border-gray-200 p-4 transition-colors duration-300 hover:bg-gray-50">
            <Link href={slug || "/home"} className="flex flex-col gap-3">
                <div className="space-y-1">
                    <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
                    <p className="text-sm text-gray-600">{excerpt}</p>
                </div>

                <div className="flex flex-wrap items-center gap-2 text-xs text-gray-500">
                    <div className="flex items-center gap-1.5">
                        <div
                            className="flex h-6 w-6 items-center justify-center rounded-full bg-gray-900 text-xs font-medium text-white">
                            {authorName[0]}
                        </div>
                        <span className="text-gray-700">{authorName}</span>
                    </div>
                    <Separator orientation="vertical" className="!h-4"/>
                    <span className="inline-flex items-center gap-1">
                        <CalendarDays className="h-3.5 w-3.5"/>
                        {publishedAt}
                    </span>
                    <Separator orientation="vertical" className="!h-4"/>
                    <span className="inline-flex items-center gap-1">
                        <Clock3 className="h-3.5 w-3.5"/>
                        {readingTime}
                    </span>
                </div>

                {tags.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                        {tags.map((tag) => (
                            <span
                                key={tag}
                                className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-2.5 py-1 text-xs text-gray-700"
                            >
                                <Hash className="h-3 w-3"/>
                                {tag}
                            </span>
                        ))}
                    </div>
                )}
            </Link>
        </article>
    );
}
