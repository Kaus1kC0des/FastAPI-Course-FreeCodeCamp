"use client";

import {useInfiniteQuery} from "@tanstack/react-query";
import {api} from "@/lib/api";
import {useAuth} from "@clerk/nextjs";
import {mapPostForCard} from "@/lib/utils";


export const useBookmarkedPosts = (limit) => {
    const {getToken} = useAuth();
    return useInfiniteQuery({
        queryKey: ["bookmarks"],
        queryFn: async ({pageParam = 0}) => {
            const token = await getToken();
            const res = await api.get("/posts/bookmarks", {
                headers: {Authorization: `Bearer ${token}`},
                params: {limit, offset: pageParam}
            });
            return Array.isArray(res.data) ? res.data.map(mapPostForCard) : [];
        },
        getNextPageParam: (lastPage, allPages) => {
            if (lastPage.length === limit) {
                return allPages.length * limit;
            }
            return undefined;
        },
        initialPageParam: 0,
    });
};