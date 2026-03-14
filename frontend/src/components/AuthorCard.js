export default function AuthorCard({author}) {
    const authorName = author?.name || "Unknown author";

    return (
        <article className="rounded-xl border border-gray-200 p-4 transition-colors duration-300 hover:bg-gray-50">
            <div className="flex gap-4">
                <div
                    className="flex h-14 w-14 shrink-0 items-center justify-center rounded-md bg-gray-900 text-lg font-semibold text-white"
                    style={author?.image ? {
                        backgroundImage: `url(${author.image})`,
                        backgroundSize: "cover",
                        backgroundPosition: "center",
                    } : undefined}
                    aria-label={authorName}
                >
                    {!author?.image && authorName[0]}
                </div>
                <div className="space-y-2">
                    <div>
                        <h3 className="text-base font-semibold text-gray-900">{authorName}</h3>
                        {author?.role && <p className="text-xs text-gray-500">{author.role}</p>}
                    </div>
                    <p className="text-sm text-gray-600">{author?.bio || "No bio available yet."}</p>
                </div>
            </div>
        </article>
    );
}
