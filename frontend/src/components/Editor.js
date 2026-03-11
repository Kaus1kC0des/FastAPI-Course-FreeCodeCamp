"use client";

import "@blocknote/core/fonts/inter.css";
import {useCreateBlockNote} from "@blocknote/react";
import {BlockNoteView} from "@blocknote/shadcn";
import "@blocknote/shadcn/style.css";

export default function Editor({setContent, onEditorReady}) {
    const editor = useCreateBlockNote();

    if (onEditorReady) onEditorReady(editor);

    return (
        <BlockNoteView
            editor={editor}
            shadCNComponents={{}}
            theme="light"
            onChange={() => {
                const nonEmptyBlocks = editor.document.filter(block => block.content.length > 0);
                const html = editor.blocksToHTMLLossy(nonEmptyBlocks);
                const cleaned = html.replace(/<[^>]+><\/[^>]+>/g, "").trim();
                setContent(cleaned);
            }}
        />
    );
}
