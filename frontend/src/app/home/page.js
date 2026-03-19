"use client";
import PostCard from "@/components/PostCard";
import {AlertMessage} from "@/components/AlertMessage";
import {Skeleton} from "@/components/ui/skeleton";
import {usePosts} from "@/app/hooks/usePosts";
import {Button} from "@/components/ui/button";

export default function HomePage() {
    const {data, isLoading, isError, error, fetchNextPage, hasNextPage, isFetchingNextPage} = usePosts(20);

    const allPosts = data?.pages.flat() || [];

    return (
        <main className="mx-auto w-full max-w-6xl px-6 py-10">
            <section className="mb-8 space-y-2">
                <h1 className="text-3xl font-bold text-gray-900">Latest stories</h1>
                <p className="text-sm text-gray-600">Catch up with the latest news...</p>
            </section>

            <section className="space-y-4">
                {isError && <AlertMessage title="Error" message={error?.message || "Failed to load posts"}/>}

                {isLoading && (
                    <>
                        <Skeleton className="h-40 w-full rounded-xl"/>
                        <Skeleton className="h-40 w-full rounded-xl"/>
                        <Skeleton className="h-40 w-full rounded-xl"/>
                    </>
                )}

                {!isLoading && !isError && allPosts.length === 0 && (
                    <p className="text-sm text-gray-500">No posts yet.</p>
                )}

                {!isLoading && !isError && allPosts.map((post) => (
                    <PostCard key={post.id} post={post}/>
                ))}

                {hasNextPage && (
                    <div className="flex justify-center py-8">
                        <Button
                            onClick={() => fetchNextPage()}
                            disabled={isFetchingNextPage}
                            variant="outline"
                            size="lg"
                        >
                            {isFetchingNextPage ? "Loading..." : "Load More"}
                        </Button>
                    </div>
                )}
            </section>
        </main>
    );
}
