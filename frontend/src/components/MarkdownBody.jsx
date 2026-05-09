import ReactMarkdown from "react-markdown";

const components = {
    h1: ({ children, ...props }) => (
        <h1 className="mt-4 text-base font-semibold tracking-tight text-white first:mt-0 sm:text-lg" {...props}>
            {children}
        </h1>
    ),
    h2: ({ children, ...props }) => (
        <h2 className="mt-3 text-sm font-semibold tracking-tight text-white first:mt-0 sm:text-base" {...props}>
            {children}
        </h2>
    ),
    h3: ({ children, ...props }) => (
        <h3 className="mt-3 text-sm font-semibold text-slate-100 first:mt-0" {...props}>
            {children}
        </h3>
    ),
    p: ({ children, ...props }) => (
        <p className="my-2 leading-relaxed first:mt-0 last:mb-0 [&+*]:mt-2" {...props}>
            {children}
        </p>
    ),
    strong: ({ children, ...props }) => (
        <strong className="font-semibold text-white" {...props}>
            {children}
        </strong>
    ),
    em: ({ children, ...props }) => (
        <em className="italic text-slate-200" {...props}>
            {children}
        </em>
    ),
    ul: ({ children, ...props }) => (
        <ul className="my-2 list-disc space-y-1 pl-5 first:mt-0 last:mb-0" {...props}>
            {children}
        </ul>
    ),
    ol: ({ children, ...props }) => (
        <ol className="my-2 list-decimal space-y-1 pl-5 first:mt-0 last:mb-0" {...props}>
            {children}
        </ol>
    ),
    li: ({ children, ...props }) => (
        <li className="leading-relaxed [&>p]:my-0" {...props}>
            {children}
        </li>
    ),
    a: ({ children, href, ...props }) => (
        <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="font-medium text-sky-400 underline decoration-sky-600/50 underline-offset-2 hover:text-sky-300"
            {...props}
        >
            {children}
        </a>
    ),
    code: ({ className, children, ...props }) => {
        const isBlock = className?.includes("language-");
        if (isBlock) {
            return (
                <code className={className} {...props}>
                    {children}
                </code>
            );
        }
        return (
            <code
                className="rounded bg-slate-950 px-1.5 py-0.5 font-mono text-[0.8125rem] text-sky-200"
                {...props}
            >
                {children}
            </code>
        );
    },
    pre: ({ children, ...props }) => (
        <pre
            className="my-3 overflow-x-auto rounded-lg border border-slate-700 bg-slate-950 p-3 text-[0.8125rem] first:mt-0 last:mb-0"
            {...props}
        >
            {children}
        </pre>
    ),
    blockquote: ({ children, ...props }) => (
        <blockquote
            className="my-2 border-l-2 border-slate-600 pl-3 text-slate-300 italic first:mt-0 last:mb-0"
            {...props}
        >
            {children}
        </blockquote>
    ),
    hr: (props) => <hr className="my-4 border-slate-700" {...props} />,
};

/** Renders assistant markdown: ## headings, **bold**, lists, `code`, fences. */
export default function MarkdownBody({ children }) {
    return (
        <div className="break-words text-slate-100">
            <ReactMarkdown components={components}>{children}</ReactMarkdown>
        </div>
    );
}
