"use client";

import {api} from "@/lib/api";
import {useInfiniteQuery} from "@tanstack/react-query";
import {useAuth} from "@clerk/nextjs";
import {mapPostForCard} from "@/lib/utils";

export const usePosts = (limit = 20) => {
    const {getToken} = useAuth();

    return useInfiniteQuery({
        queryKey: ["posts"],
        queryFn: async ({pageParam = 0}) => {
            const token = await getToken();
            const res = await api.get("/posts/all", {
                headers: {Authorization: `Bearer ${token}`},
                params: {offset: pageParam, limit}
            });
            return Array.isArray(res.data) ? res.data.map(mapPostForCard) : [];
        },
        getNextPageParam: (lastPage, allPages) => {
            // if last page was full, there's more data
            if (lastPage.length === limit) {
                return allPages.length * limit;  // next offset
            }
            return undefined;  // no more pages
        },
        initialPageParam: 0,
    });
};