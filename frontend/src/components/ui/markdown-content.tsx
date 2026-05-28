'use client'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { cn } from '@/lib/utils'

interface MarkdownContentProps {
    content: string
    className?: string
}

export function MarkdownContent({ content, className }: MarkdownContentProps) {
    return (
        <div className={cn('markdown-content', className)}>
            <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                    // Code blocks
                    code({ className, children, ...props }) {
                        const match = /language-(\w+)/.exec(className || '')
                        const isInline = !match && !String(children).includes('\n')

                        if (isInline) {
                            return (
                                <code
                                    className="bg-muted px-1.5 py-0.5 rounded text-base font-mono text-primary"
                                    {...props}
                                >
                                    {children}
                                </code>
                            )
                        }

                        return (
                            <SyntaxHighlighter
                                style={oneDark}
                                language={match?.[1] ?? 'text'}
                                PreTag="div"
                                customStyle={{
                                    borderRadius: '0.5rem',
                                    fontSize: '0.875rem',
                                    margin: '1rem 0',
                                    padding: '1rem',
                                }}
                                showLineNumbers={false}
                            >
                                {String(children).replace(/\n$/, '')}
                            </SyntaxHighlighter>
                        )
                    },

                    // Headings
                    h1: ({ children }) => (
                        <h1 className="text-3xl font-bold mt-8 mb-4 text-foreground first:mt-0">
                            {children}
                        </h1>
                    ),
                    h2: ({ children }) => (
                        <h2 className="text-xl font-semibold mt-6 mb-3 text-foreground border-b border-border pb-1">
                            {children}
                        </h2>
                    ),
                    h3: ({ children }) => (
                        <h3 className="text-lg font-medium mt-4 mb-2 text-foreground">
                            {children}
                        </h3>
                    ),

                    // Paragraphs
                    p: ({ children }) => (
                        <p className="text-base leading-relaxed text-muted-foreground mb-3">
                            {children}
                        </p>
                    ),

                    // Lists
                    ul: ({ children }) => (
                        <ul className="my-3 space-y-1 pl-5 list-none">
                            {children}
                        </ul>
                    ),
                    ol: ({ children }) => (
                        <ol className="my-3 space-y-1 pl-5 list-decimal text-base text-muted-foreground">
                            {children}
                        </ol>
                    ),
                    li: ({ children }) => (
                        <li className="text-base text-muted-foreground flex items-start gap-2">
                            <span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-primary/60 shrink-0" />
                            <span>{children}</span>
                        </li>
                    ),

                    // Emphasis
                    strong: ({ children }) => (
                        <strong className="font-semibold text-foreground">{children}</strong>
                    ),
                    em: ({ children }) => (
                        <em className="italic text-muted-foreground">{children}</em>
                    ),

                    // Blockquote
                    blockquote: ({ children }) => (
                        <blockquote className="border-l-2 border-primary/50 pl-4 my-4 italic text-base text-muted-foreground bg-muted/30 py-2 pr-4 rounded-r">
                            {children}
                        </blockquote>
                    ),

                    // Tables
                    table: ({ children }) => (
                        <div className="my-4 overflow-x-auto rounded-lg border border-border">
                            <table className="w-full text-sm">{children}</table>
                        </div>
                    ),
                    thead: ({ children }) => (
                        <thead className="bg-muted/50">{children}</thead>
                    ),
                    th: ({ children }) => (
                        <th className="px-4 py-2 text-left font-medium text-foreground text-sm uppercase tracking-wide">
                            {children}
                        </th>
                    ),
                    td: ({ children }) => (
                        <td className="px-4 py-2.5 text-muted-foreground border-t border-border text-base">
                            {children}
                        </td>
                    ),

                    // Horizontal rule
                    hr: () => <hr className="my-6 border-border" />,

                    // Links
                    a: ({ href, children }) => (
                        <a
                            href={href}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-primary underline underline-offset-2 hover:text-primary/80"
                        >
                            {children}
                        </a>
                    ),
                }}
            >
                {content}
            </ReactMarkdown>
        </div>
    )
}
