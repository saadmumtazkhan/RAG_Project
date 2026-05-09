import { useState, useRef, useEffect } from "react";
import { askQuestion } from "../api";
import { YOUTUBE_VIDEO_URL } from "../constants";
import MarkdownBody from "./MarkdownBody";

export default function ChatBox() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);

    const chatRef = useRef(null);
    const inputRef = useRef(null);

    useEffect(() => {
        chatRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, loading]);

    const handleSend = async () => {
        const trimmed = input.trim();
        if (!trimmed || loading) return;

        const userMessage = {
            role: "user",
            text: trimmed,
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        try {
            const res = await askQuestion(trimmed);

            setMessages((prev) => [
                ...prev,
                {
                    role: "bot",
                    text: res.answer,
                },
            ]);
        } catch {
            setMessages((prev) => [
                ...prev,
                {
                    role: "bot",
                    text: "Something went wrong. Check the API and try again.",
                },
            ]);
        } finally {
            setLoading(false);
            inputRef.current?.focus();
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex h-dvh min-h-0 flex-col bg-slate-950 text-slate-100 antialiased">
            <header className="shrink-0 border-b border-slate-800/80 px-4 py-3 sm:px-6">
                <div className="mx-auto max-w-3xl space-y-3">
                    <div>
                        <h1 className="text-lg font-semibold tracking-tight text-white sm:text-xl">
                            Video transcript assistant
                        </h1>
                        <p className="mt-0.5 text-xs text-slate-400 sm:text-sm">
                            Questions about one ingested YouTube video — answers come from its transcript only
                        </p>
                        <p className="mt-2 text-xs sm:text-sm">
                            <a
                                href={YOUTUBE_VIDEO_URL}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-1.5 font-medium text-sky-400 underline decoration-sky-600/50 underline-offset-2 transition-colors hover:text-sky-300"
                            >
                                Open source video on YouTube
                                <span aria-hidden className="text-sky-500/90">
                                    ↗
                                </span>
                            </a>
                        </p>
                    </div>
                    <div
                        className="rounded-xl border border-sky-900/60 bg-sky-950/40 px-3 py-2.5 text-xs leading-relaxed text-slate-300 sm:text-sm"
                        role="region"
                        aria-label="How this assistant works"
                    >
                        <p className="font-medium text-sky-200/95">What this does</p>
                        <p className="mt-1 text-slate-400">
                            This is a <span className="text-slate-300">RAG</span> chatbot: the video&apos;s transcript
                            is chunked and stored; each time you ask, the app pulls the most relevant lines and the
                            model answers <span className="text-slate-300">only from that text</span>. It is not a
                            general web assistant — topics outside the transcript may get a short redirect, not a
                            factual answer.
                        </p>
                    </div>
                </div>
            </header>

            <main
                className="min-h-0 flex-1 overflow-y-auto px-4 py-4 sm:px-6"
                aria-label="Conversation"
            >
                <div className="mx-auto flex max-w-3xl flex-col gap-3">
                    {messages.length === 0 && !loading && (
                        <div
                            className="rounded-2xl border border-dashed border-slate-700/80 bg-slate-900/40 px-4 py-8 text-center sm:py-10"
                            role="status"
                        >
                            <p className="text-sm font-medium text-slate-300">Ask about the video</p>
                            <p className="mt-2 text-sm text-slate-500">
                                Try summarizing a section, asking who said what, or clarifying a term mentioned in the
                                transcript.
                            </p>
                            <p className="mt-4 text-xs text-slate-600">
                                <kbd className="rounded border border-slate-600 bg-slate-800 px-1.5 py-0.5 font-mono text-slate-400">
                                    Enter
                                </kbd>{" "}
                                send ·{" "}
                                <kbd className="rounded border border-slate-600 bg-slate-800 px-1.5 py-0.5 font-mono text-slate-400">
                                    Shift+Enter
                                </kbd>{" "}
                                new line
                            </p>
                        </div>
                    )}

                    {messages.map((msg, i) => (
                        <div
                            key={i}
                            className={`flex w-full ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                        >
                            <div
                                className={`max-w-[min(100%,42rem)] rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm sm:text-[0.9375rem] ${
                                    msg.role === "user"
                                        ? "bg-sky-600 text-white"
                                        : "border border-slate-700/80 bg-slate-900 text-slate-100"
                                }`}
                            >
                                {msg.role === "user" ? (
                                    <p className="whitespace-pre-wrap break-words">{msg.text}</p>
                                ) : (
                                    <MarkdownBody>{msg.text}</MarkdownBody>
                                )}
                            </div>
                        </div>
                    ))}

                    {loading && (
                        <div className="flex justify-start">
                            <div
                                className="flex items-center gap-2 rounded-2xl border border-slate-700/80 bg-slate-900 px-4 py-3 text-sm text-slate-400"
                                aria-live="polite"
                                aria-busy="true"
                            >
                                <span
                                    className="inline-flex size-2 animate-pulse rounded-full bg-sky-500"
                                    aria-hidden
                                />
                                <span className="inline-flex size-2 animate-pulse rounded-full bg-sky-500 [animation-delay:150ms]" aria-hidden />
                                <span className="inline-flex size-2 animate-pulse rounded-full bg-sky-500 [animation-delay:300ms]" aria-hidden />
                                <span className="sr-only">Assistant is replying</span>
                                <span className="pl-1">Thinking…</span>
                            </div>
                        </div>
                    )}

                    <div ref={chatRef} />
                </div>
            </main>

            <footer className="shrink-0 border-t border-slate-800/80 bg-slate-950/95 px-4 py-3 pb-[max(0.75rem,env(safe-area-inset-bottom))] backdrop-blur sm:px-6">
                <form
                    className="mx-auto flex max-w-3xl flex-col gap-2 sm:flex-row sm:items-end"
                    onSubmit={(e) => {
                        e.preventDefault();
                        handleSend();
                    }}
                    aria-busy={loading}
                >
                    <label htmlFor="rag-input" className="sr-only">
                        Your question
                    </label>
                    <textarea
                        id="rag-input"
                        ref={inputRef}
                        rows={2}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask something about the video…"
                        disabled={loading}
                        className="min-h-[2.75rem] w-full resize-y rounded-xl border border-slate-700 bg-slate-900 px-3 py-2.5 text-sm text-white placeholder:text-slate-500 focus:border-sky-500/80 focus:outline-none focus:ring-2 focus:ring-sky-500/30 disabled:cursor-not-allowed disabled:opacity-60 sm:min-h-[3rem] sm:flex-1"
                    />
                    <button
                        type="submit"
                        disabled={loading || !input.trim()}
                        className="h-11 shrink-0 rounded-xl bg-sky-600 px-5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-sky-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-400 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400 disabled:shadow-none sm:h-12 sm:self-stretch sm:px-6"
                    >
                        {loading ? "Sending…" : "Send"}
                    </button>
                </form>
            </footer>
        </div>
    );
}
