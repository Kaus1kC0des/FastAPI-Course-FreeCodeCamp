"use client";

import {useMutation, useQueryClient} from "@tanstack/react-query";
import {api} from "@/lib/api";
import {useAuth} from "@clerk/nextjs";

export const useBookmark = () => {
    const {getToken} = useAuth();
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async ({postId, isBookmarked}) => {
            const token = await getToken();
            const endpoint = `/posts/bookmark/${postId}`;

            if (isBookmarked) {
                // Unbookmark - DELETE
                return api.delete(endpoint, {
                    headers: {Authorization: `Bearer ${token}`}
                });
            } else {
                // Bookmark - POST
                return api.post(endpoint, null, {
                    headers: {Authorization: `Bearer ${token}`}
                });
            }
        },
        onMutate: async ({postId, isBookmarked}) => {

            // Cancel ongoing queries
            await queryClient.cancelQueries({queryKey: ["posts"]});
            await queryClient.cancelQueries({queryKey: ["post", postId]});
            await queryClient.cancelQueries({queryKey: ["bookmarks"]});

            // Snapshot previous values
            const previousPosts = queryClient.getQueryData(["posts"]);
            const previousPost = queryClient.getQueryData(["post", postId]);
            const previousBookmarks = queryClient.getQueryData(["bookmarks"]);

            // Optimistically update the posts list cache
            queryClient.setQueryData(["posts"], (old) => {
                if (!old?.pages) return old;

                return {
                    ...old,
                    pages: old.pages.map(page =>
                        page.map(post =>
                            post.id === postId
                                ? {...post, isBookmarked: !isBookmarked}
                                : post
                        )
                    )
                };
            });

            // Optimistically update the individual post cache
            queryClient.setQueryData(["post", postId], (old) => {
                if (!old) return old;
                return {...old, isBookmarked: !isBookmarked};
            });

            // Optimistically update the bookmarks cache
            queryClient.setQueryData(["bookmarks"], (old) => {
                if (!old?.pages) return old;

                // If unbookmarking, remove from bookmarks list
                if (isBookmarked) {
                    return {
                        ...old,
                        pages: old.pages.map(page =>
                            page.filter(post => post.id !== postId)
                        )
                    };
                } else {
                    // If bookmarking, just update the flag (post won't be in this list yet)
                    return {
                        ...old,
                        pages: old.pages.map(page =>
                            page.map(post =>
                                post.id === postId
                                    ? {...post, isBookmarked: true}
                                    : post
                            )
                        )
                    };
                }
            });

            console.log("onMutate - after update, new state:", !isBookmarked);
            return {previousPosts, previousPost, previousBookmarks};
        },
        onError: (err, {postId}, context) => {
            // Rollback on error
            if (context?.previousPosts) {
                queryClient.setQueryData(["posts"], context.previousPosts);
            }
            if (context?.previousPost) {
                queryClient.setQueryData(["post", postId], context.previousPost);
            }
            if (context?.previousBookmarks) {
                queryClient.setQueryData(["bookmarks"], context.previousBookmarks);
            }
            console.error("Bookmark error:", err);
        },
        onSettled: (data, error, {postId}) => {
            // Refetch to sync with backend
            queryClient.invalidateQueries({queryKey: ["posts"]});
            queryClient.invalidateQueries({queryKey: ["post", postId]});
            queryClient.invalidateQueries({queryKey: ["bookmarks"]});
        }
    });
};
