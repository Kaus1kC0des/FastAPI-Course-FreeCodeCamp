"use client";

import {useQuery} from "@tanstack/react-query";
import {api} from "@/lib/api";
import {useAuth} from "@clerk/nextjs";

export const usePost = (postId) => {
    const {getToken} = useAuth();

    return useQuery({
        queryKey: ["post", postId],
        queryFn: async () => {
            const token = await getToken();
            const res = await api.get(`/posts/${postId}`, {
                headers: {Authorization: `Bearer ${token}`},
            });
            return res.data;
        },
        enabled: !!postId,
    });
};
