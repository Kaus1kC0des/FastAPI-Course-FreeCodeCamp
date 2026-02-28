"use client";

import "@blocknote/core/fonts/inter.css";
import {useCreateBlockNote} from "@blocknote/react";
import {BlockNoteView} from "@blocknote/shadcn";
import "@blocknote/shadcn/style.css";

export default function App() {
    const editor = useCreateBlockNote();

    return (
        <BlockNoteView
            editor={editor}
            shadCNComponents={{}}
            theme="light"
        />
    );
}
