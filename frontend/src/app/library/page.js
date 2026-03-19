"use client";

import PostCard from "@/components/PostCard";
import {AlertMessage} from "@/components/AlertMessage";
import {Skeleton} from "@/components/ui/skeleton";
import {useBookmarkedPosts} from "@/app/hooks/useBookmarkedPosts";
import InfiniteScroll from "react-infinite-scroll-component";

export default function Library() {
    const {data, isLoading, isError, error, fetchNextPage, hasNextPage} = useBookmarkedPosts(20);
    const allBookmarks = data?.pages.flat() || [];

    if (isLoading) {
        return (
            <main className="mx-auto w-full max-w-6xl px-6 py-10">
                <section className="mb-8 space-y-2">
                    <h1 className="text-3xl font-bold text-gray-900">Your Library</h1>
                    <p className="text-sm text-gray-600">Your saved stories...</p>
                </section>
                <section className="space-y-4">
                    <Skeleton className="h-40 w-full rounded-xl"/>
                    <Skeleton className="h-40 w-full rounded-xl"/>
                    <Skeleton className="h-40 w-full rounded-xl"/>
                </section>
            </main>
        );
    }

    if (isError) {
        return (
            <main className="mx-auto w-full max-w-6xl px-6 py-10">
                <AlertMessage title="Error" message={error?.message || "Failed to load bookmarks"}/>
            </main>
        );
    }

    if (allBookmarks.length === 0) {
        return (
            <main className="mx-auto w-full max-w-6xl px-6 py-10">
                <section className="mb-8 space-y-2">
                    <h1 className="text-3xl font-bold text-gray-900">Your Library</h1>
                    <p className="text-sm text-gray-600">Your saved stories...</p>
                </section>
                <p className="text-sm text-gray-500">No bookmarks yet. Start saving stories you love!</p>
            </main>
        );
    }

    return (
        <main className="mx-auto w-full max-w-6xl px-6 py-10">
            <section className="mb-8 space-y-2">
                <h1 className="text-3xl font-bold text-gray-900">Your Library</h1>
                <p className="text-sm text-gray-600">Your saved stories...</p>
            </section>

            <InfiniteScroll
                dataLength={allBookmarks.length}
                next={fetchNextPage}
                hasMore={hasNextPage}
                loader={
                    <div className="py-4 space-y-4">
                        <Skeleton className="h-40 w-full rounded-xl"/>
                        <Skeleton className="h-40 w-full rounded-xl"/>
                    </div>
                }
                endMessage={
                    <p className="text-center py-8 text-sm text-gray-500">
                        You've reached the end of your library!
                    </p>
                }
            >
                <section className="space-y-4">
                    {allBookmarks.map((bookmark) => (
                        <PostCard key={bookmark.id} post={bookmark}/>
                    ))}
                </section>
            </InfiniteScroll>
        </main>
    );
}