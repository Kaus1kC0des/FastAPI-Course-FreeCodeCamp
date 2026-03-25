"use client";

import {useMutation, useQueryClient} from "@tanstack/react-query";
import {api} from "@/lib/api";
import {useAuth} from "@clerk/nextjs";

export const useLike = () => {
    const {getToken} = useAuth();
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async ({postId, isLiked}) => {
            const token = await getToken();
            const normalizedPostId = Number(postId);
            const endpoint = `/posts/like/${normalizedPostId}`;

            if (isLiked) {
                return api.delete(endpoint, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
            } else {
                return api.post(endpoint, null, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
            }
        },
        onMutate: async ({postId, isLiked}) => {
            const normalizedPostId = Number(postId);
            await queryClient.cancelQueries({queryKey: ["posts"]});
            await queryClient.cancelQueries({queryKey: ["post"]});
            await queryClient.cancelQueries({queryKey: ["bookmarks"]});

            const previousPosts = queryClient.getQueryData(["posts"]);
            const previousPostQueries = queryClient.getQueriesData({queryKey: ["post"]});
            const previousBookmarks = queryClient.getQueryData(["bookmarks"]);
            const delta = isLiked ? -1 : 1;
            const updatePostLikeState = (post) => {
                const currentLikesCount = post.likesCount ?? post.likes_count ?? 0;
                const nextLikesCount = Math.max(0, Number(currentLikesCount) + delta);
                return {
                    ...post,
                    isLiked: !isLiked,
                    is_liked: !isLiked,
                    likesCount: nextLikesCount,
                    likes_count: nextLikesCount,
                };
            };

            queryClient.setQueryData(["posts"], (old) => {
                if (!old?.pages) return old;

                return {
                    ...old,
                    pages: old.pages.map(page =>
                        page.map(post =>
                            Number(post.id) === normalizedPostId
                                ? updatePostLikeState(post)
                                : post
                        )
                    )
                };
            });
            queryClient.setQueriesData({queryKey: ["post"]}, (old) => {
                if (!old || Number(old.id) !== normalizedPostId) return old;
                return updatePostLikeState(old);
            });
            queryClient.setQueryData(["bookmarks"], (old) => {
                if (!old?.pages) return old;
                return {
                    ...old,
                    pages: old.pages.map(page =>
                        page.map(post =>
                            Number(post.id) === normalizedPostId
                                ? updatePostLikeState(post)
                                : post
                        )
                    )
                };
            });
            return {previousPosts, previousPostQueries, previousBookmarks};
        },
        onError: (err, _variables, context) => {
            // Rollback on error
            if (context?.previousPosts) {
                queryClient.setQueryData(["posts"], context.previousPosts);
            }
            if (context?.previousPostQueries) {
                context.previousPostQueries.forEach(([queryKey, data]) => {
                    queryClient.setQueryData(queryKey, data);
                });
            }
            if (context?.previousBookmarks) {
                queryClient.setQueryData(["bookmarks"], context.previousBookmarks);
            }
            console.error("Like error:", err);
        },
        onSettled: () => {
            // Refetch to sync with backend
            queryClient.invalidateQueries({queryKey: ["posts"]});
            queryClient.invalidateQueries({queryKey: ["post"]});
            queryClient.invalidateQueries({queryKey: ["bookmarks"]});
        }
    });
};
