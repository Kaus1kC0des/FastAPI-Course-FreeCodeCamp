"use client";
import PostCard from "@/components/PostCard";
import AuthorCard from "@/components/AuthorCard";
import {useEffect, useState} from "react";
import {api} from "@/lib/api";
import {useAuth} from "@clerk/nextjs";
import {AlertMessage} from "@/components/AlertMessage";
import {Skeleton} from "@/components/ui/skeleton";

function toPlainText(html) {
    if (!html) return "";
    return html.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
}

function toReadingTime(text) {
    const words = text ? text.split(/\s+/).length : 0;
    const minutes = Math.max(1, Math.ceil(words / 200));
    return `${minutes} min read`;
}

function toDisplayDate(isoDate) {
    if (!isoDate) return "Unknown date";
    return new Date(isoDate).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
    });
}

function mapPostForCard(post) {
    const plainText = toPlainText(post.content || "");
    const authorUsername = post.author?.username || "unknown";
    const authorName = [post.author?.first_name, post.author?.last_name]
        .filter(Boolean)
        .join(" ")
        .trim() || post.author?.username || "Unknown author";

    return {
        id: post.id,
        slug: `/story/${encodeURIComponent(authorUsername)}/${post.id}`,
        title: post.title || "Untitled",
        excerpt: plainText
            ? plainText.slice(0, 180) + (plainText.length > 180 ? "..." : "")
            : "Click to open and read this story.",
        publishedAt: toDisplayDate(post.created_at),
        readingTime: plainText ? toReadingTime(plainText) : "1 min read",
        tags: (post.tags || []).map((tag) => tag.tag),
        author: {
            id: post.author?.id,
            name: authorName,
            role: post.author?.role || "Author",
            bio: post.author?.email || "No bio available yet.",
            image: post.author?.image || null,
        },
    };
}

export default function HomePage() {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const {getToken} = useAuth();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = await getToken();
                const response = await api.get("/posts/all", {
                    headers: {Authorization: `Bearer ${token}`},
                });
                const mappedPosts = Array.isArray(response.data)
                    ? response.data.map(mapPostForCard)
                    : [];
                setPosts(mappedPosts);
            } catch (err) {
                setError({
                    title: "Failed to load posts",
                    message: err?.response?.data?.detail || "Could not fetch posts from backend.",
                });
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [getToken]);

    const authors = Array.from(
        new Map(posts.map((post) => [post.author.id || post.author.name, post.author])).values()
    );

    return (
        <main className="mx-auto w-full max-w-6xl px-6 py-10">
            <section className="mb-8 space-y-2">
                <h1 className="text-3xl font-bold text-gray-900">Latest stories</h1>
                <p className="text-sm text-gray-600">Real posts fetched from your backend API.</p>
            </section>

            <section className="grid grid-cols-1 gap-8 lg:grid-cols-[2fr_1fr]">
                <div className="space-y-4">
                    {error && <AlertMessage title={error.title} message={error.message}/>}

                    {loading && (
                        <>
                            <Skeleton className="h-40 w-full rounded-xl"/>
                            <Skeleton className="h-40 w-full rounded-xl"/>
                            <Skeleton className="h-40 w-full rounded-xl"/>
                        </>
                    )}

                    {!loading && !error && posts.length === 0 && (
                        <p className="text-sm text-gray-500">No posts found yet.</p>
                    )}

                    {!loading && !error && posts.map((post) => (
                        <PostCard key={post.id} post={post}/>
                    ))}
                </div>

                <aside className="space-y-4">
                    <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-500">Author details</h2>
                    {authors.length === 0 && !loading && (
                        <p className="text-sm text-gray-500">No authors to show yet.</p>
                    )}
                    {authors.map((author) => (
                        <AuthorCard key={author.id || author.name} author={author}/>
                    ))}
                </aside>
            </section>
        </main>
    );
}
