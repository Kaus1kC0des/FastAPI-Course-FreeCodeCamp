"use client";
import PostCard from "@/components/PostCard";
import {useEffect, useState} from "react";
import {useParams} from "next/navigation";
import {api} from "@/lib/api";
import {useAuth} from "@clerk/nextjs";
import {AlertMessage} from "@/components/AlertMessage";
import {Skeleton} from "@/components/ui/skeleton";
import {mapPostForCard} from "@/lib/utils";


export default function HomePage() {
    const {tag} = useParams();
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const {getToken} = useAuth();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = await getToken();
                const response = await api.get(`/posts/tags/${tag}`, {
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
    }, [getToken, tag]);

    return (
        <main className="mx-auto w-full max-w-6xl px-6 py-10">
            <section className="mb-8 space-y-2">
                <h1 className="text-3xl font-bold text-gray-900">#{tag} stories</h1>
                <p className="text-sm text-gray-600">Posts filtered by this tag.</p>
            </section>

            <section className="space-y-4">
                {error && <AlertMessage title={error.title} message={error.message}/>}

                {loading && (
                    <>
                        <Skeleton className="h-40 w-full rounded-xl"/>
                        <Skeleton className="h-40 w-full rounded-xl"/>
                        <Skeleton className="h-40 w-full rounded-xl"/>
                    </>
                )}

                {!loading && !error && posts.length === 0 && (
                    <p className="text-sm text-gray-500">No posts yet.</p>
                )}

                {!loading && !error && posts.map((post) => (
                    <PostCard key={post.id} post={post}/>
                ))}
            </section>
        </main>
    );
}
