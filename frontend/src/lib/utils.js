import {clsx} from "clsx";
import {twMerge} from "tailwind-merge"
import {api} from "@/lib/api";

export function cn(...inputs) {
    return twMerge(clsx(inputs));
}

export function toDisplayDate(isoDate) {
    if (!isoDate) return "Unknown date";
    return new Date(isoDate).toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric",
    });
}

export function toReadingTime(html) {
    const plainText = (html || "").replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
    const words = plainText ? plainText.split(" ").length : 0;
    return `${Math.max(1, Math.ceil(words / 200))} min read`;
}

export function toPlainText(html) {
    if (!html) return "";
    return html.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
}

export function mapPostForCard(post) {
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
        isBookmarked: Boolean(post.isBookmarked ?? post.is_bookmarked),
        isLiked: Boolean(post.isLiked ?? post.is_liked),
        likesCount: Number(post.likesCount ?? post.likes_count ?? 0),
    };
}

const toggleBookmark = async (postId, currentState, getToken, setPosts) => {
    try {
        const token = await getToken();

        if (!currentState) {
            await api.post(`/posts/bookmark/${postId}`, null, {
                headers: {Authorization: `Bearer ${token}`},
            });
        } else {
            await api.delete(`/posts/bookmark/${postId}`, {
                headers: {Authorization: `Bearer ${token}`},
            });
        }
        setPosts((prevPosts) =>
            prevPosts.map((p) =>
                p.id === postId
                    ? {...p, isBookmarked: !currentState}
                    : p
            )
        );

    } catch (err) {
        console.error("Bookmark error:", err);
    }
};

export async function fetchPosts(token) {
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
