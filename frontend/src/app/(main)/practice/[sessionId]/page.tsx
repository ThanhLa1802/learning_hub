'use client'

import { useEffect, useRef, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft, Send, StopCircle } from 'lucide-react'
import { sessionsApi } from '@/lib/apiClient'
import { useLang } from '@/contexts/LangContext'
import { PracticeSession, SessionMessage } from '@/types'
import { Button } from '@/components/ui/button'
import { ButtonLink } from '@/components/ui/button-link'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { toast } from 'sonner'

export default function PracticeSessionPage() {
    const { sessionId } = useParams<{ sessionId: string }>()
    const router = useRouter()
    const { lang } = useLang()
    const [session, setSession] = useState<PracticeSession | null>(null)
    const [messages, setMessages] = useState<SessionMessage[]>([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const [completing, setCompleting] = useState(false)
    const [streamingContent, setStreamingContent] = useState('')
    const messagesEndRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        sessionsApi.getById(sessionId).then((r) => {
            const s = r.data
            if (s.status === 'completed') {
                router.replace(`/practice/${sessionId}/result`)
                return
            }
            setSession(s)
            setMessages(s.messages)
        })
    }, [sessionId, router])

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages, streamingContent])

    const handleSendMessage = async () => {
        if (!input.trim() || loading) return
        const content = input.trim()
        setInput('')
        setLoading(true)
        setStreamingContent('')
        try {
            const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
            const res = await fetch(`${API_URL}/api/v1/sessions/${sessionId}/messages/stream`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ content }),
            })
            if (!res.ok || !res.body) {
                throw new Error('Stream failed')
            }
            const reader = res.body.getReader()
            const decoder = new TextDecoder()
            let buffer = ''
            let fullAiContent = ''
            let aiMsgId = ''
            while (true) {
                const { done, value } = await reader.read()
                if (done) break
                buffer += decoder.decode(value, { stream: true })
                const lines = buffer.split('\n')
                buffer = lines.pop() ?? ''
                for (const line of lines) {
                    if (!line.startsWith('data: ')) continue
                    const data = JSON.parse(line.slice(6))
                    if (data.type === 'user_msg') {
                        setMessages((prev) => [
                            ...prev,
                            { id: data.id, session_id: sessionId, role: 'user' as const, content: data.content, created_at: new Date().toISOString() },
                        ])
                    } else if (data.type === 'token') {
                        fullAiContent += data.content
                        setStreamingContent(fullAiContent)
                    } else if (data.type === 'done') {
                        aiMsgId = data.id
                        setMessages((prev) => [
                            ...prev,
                            { id: aiMsgId, session_id: sessionId, role: 'assistant' as const, content: fullAiContent, created_at: new Date().toISOString() },
                        ])
                        setStreamingContent('')
                    }
                }
            }
        } catch {
            toast.error('Failed to send message')
        } finally {
            setLoading(false)
        }
    }

    const handleComplete = async (userResponse?: string) => {
        setCompleting(true)
        try {
            await sessionsApi.complete(sessionId, { user_response: userResponse, lang })
            router.push(`/practice/${sessionId}/result`)
        } catch {
            toast.error('Failed to complete session')
            setCompleting(false)
        }
    }

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
            e.preventDefault()
            if (session?.mode === 'ai_chat') {
                handleSendMessage()
            }
        }
    }

    if (!session) {
        return (
            <div className="flex justify-center py-20">
                <div className="h-8 w-8 rounded-full border-2 border-primary border-t-transparent animate-spin" />
            </div>
        )
    }

    return (
        <div className="max-w-3xl space-y-4">
            <div className="flex items-center justify-between">
                <ButtonLink href="/dashboard" variant="ghost" size="sm">
                    <ArrowLeft className="h-4 w-4 mr-1" />
                    Dashboard
                </ButtonLink>
                <Badge variant="outline">{session.scenario?.category?.title}</Badge>
            </div>

            <div>
                <h1 className="text-xl font-bold">{session.scenario?.title}</h1>
                <p className="text-sm text-muted-foreground mt-0.5">
                    {session.mode === 'ai_chat' ? 'AI Roleplay Chat' : 'Written Response'}
                </p>
            </div>

            {session.mode === 'text_response' ? (
                <TextResponseMode session={session} onComplete={handleComplete} completing={completing} />
            ) : (
                <ChatMode
                    session={session}
                    messages={messages}
                    streamingContent={streamingContent}
                    input={input}
                    loading={loading}
                    completing={completing}
                    onInputChange={setInput}
                    onSend={handleSendMessage}
                    onComplete={() => handleComplete()}
                    onKeyDown={handleKeyDown}
                    messagesEndRef={messagesEndRef}
                />
            )}
        </div>
    )
}

function TextResponseMode({
    session,
    onComplete,
    completing,
}: {
    session: PracticeSession
    onComplete: (response: string) => void
    completing: boolean
}) {
    const [response, setResponse] = useState('')

    return (
        <div className="space-y-4">
            <Card>
                <CardHeader>
                    <CardTitle className="text-base">Your Task</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-muted-foreground leading-relaxed">{session.scenario?.description}</p>
                </CardContent>
            </Card>

            <div className="space-y-2">
                <label className="text-sm font-medium">Your Response</label>
                <Textarea
                    value={response}
                    onChange={(e) => setResponse(e.target.value)}
                    placeholder="Write your professional response here…"
                    className="min-h-[200px] resize-none font-mono text-sm"
                />
                <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">{response.length} characters</span>
                    <Button
                        onClick={() => onComplete(response)}
                        disabled={completing || response.trim().length < 20}
                        className="gap-2"
                    >
                        <Send className="h-4 w-4" />
                        {completing ? 'Evaluating…' : 'Submit & Get Feedback'}
                    </Button>
                </div>
            </div>
        </div>
    )
}

function ChatMode({
    session,
    messages,
    streamingContent,
    input,
    loading,
    completing,
    onInputChange,
    onSend,
    onComplete,
    onKeyDown,
    messagesEndRef,
}: {
    session: PracticeSession
    messages: SessionMessage[]
    streamingContent: string
    input: string
    loading: boolean
    completing: boolean
    onInputChange: (v: string) => void
    onSend: () => void
    onComplete: () => void
    onKeyDown: (e: React.KeyboardEvent) => void
    messagesEndRef: React.RefObject<HTMLDivElement | null>
}) {
    return (
        <div className="space-y-4">
            <Card>
                <CardHeader className="pb-3">
                    <CardTitle className="text-base">Your Task</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-sm text-muted-foreground leading-relaxed">{session.scenario?.description}</p>
                </CardContent>
            </Card>

            <div className="border rounded-lg bg-card min-h-[400px] max-h-[500px] overflow-y-auto flex flex-col p-4 gap-3">
                {messages.length === 0 && (
                    <p className="text-sm text-muted-foreground text-center py-8">
                        Start the conversation by typing your first message below.
                    </p>
                )}
                {messages.map((msg) => (
                    <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div
                            className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${msg.role === 'user'
                                ? 'bg-primary text-primary-foreground rounded-br-sm'
                                : 'bg-muted text-foreground rounded-bl-sm'
                                }`}
                        >
                            {msg.content}
                        </div>
                    </div>
                ))}
                {streamingContent && (
                    <div className="flex justify-start">
                        <div className="bg-muted text-foreground rounded-2xl rounded-bl-sm px-4 py-2.5 text-sm leading-relaxed max-w-[80%]">
                            {streamingContent}
                            <span className="inline-block w-0.5 h-3.5 bg-muted-foreground ml-0.5 align-middle animate-pulse" />
                        </div>
                    </div>
                )}
                {loading && !streamingContent && (
                    <div className="flex justify-start">
                        <div className="bg-muted rounded-2xl rounded-bl-sm px-4 py-2.5">
                            <div className="flex gap-1">
                                <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground animate-bounce [animation-delay:-0.3s]" />
                                <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground animate-bounce [animation-delay:-0.15s]" />
                                <span className="h-1.5 w-1.5 rounded-full bg-muted-foreground animate-bounce" />
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="flex gap-2">
                <Textarea
                    value={input}
                    onChange={(e) => onInputChange(e.target.value)}
                    onKeyDown={onKeyDown}
                    placeholder="Type your message… (Ctrl+Enter to send)"
                    className="min-h-[80px] resize-none text-sm"
                    disabled={loading || completing}
                />
                <div className="flex flex-col gap-2">
                    <Button onClick={onSend} disabled={!input.trim() || loading || completing} className="gap-1.5">
                        <Send className="h-4 w-4" />
                        Send
                    </Button>
                    <Button
                        variant="outline"
                        onClick={onComplete}
                        disabled={messages.length === 0 || loading || completing}
                        className="gap-1.5 text-xs"
                    >
                        <StopCircle className="h-4 w-4" />
                        {completing ? 'Evaluating…' : 'End & Evaluate'}
                    </Button>
                </div>
            </div>
            <p className="text-xs text-muted-foreground">
                Have a natural conversation, then click <strong>End & Evaluate</strong> to receive AI feedback on your English.
            </p>
        </div>
    )
}
