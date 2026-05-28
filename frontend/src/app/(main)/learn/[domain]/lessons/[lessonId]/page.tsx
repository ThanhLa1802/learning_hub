'use client'

import { useEffect, useState, useRef } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import {
    ArrowLeft, CheckCircle2, Clock, Lightbulb, Send, ChevronDown, ChevronUp, BookOpen, ExternalLink, ArrowRight
} from 'lucide-react'
import { lessonsApi } from '@/services/learnApi'
import { useLang } from '@/contexts/LangContext'
import { Lesson, AIExplainResponse } from '@/types/learn'
import { Button } from '@/components/ui/button'
import { ButtonLink } from '@/components/ui/button-link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Textarea } from '@/components/ui/textarea'
import { MarkdownContent } from '@/components/ui/markdown-content'
import { toast } from 'sonner'

export default function LessonPage() {
    const params = useParams()
    const router = useRouter()
    const { lang } = useLang()
    const domain = params.domain as string
    const lessonId = params.lessonId as string

    const [lesson, setLesson] = useState<Lesson | null>(null)
    const [loading, setLoading] = useState(true)
    const [completed, setCompleted] = useState(false)
    const [quizPassed, setQuizPassed] = useState(true)
    const [question, setQuestion] = useState('')
    const [aiResponse, setAiResponse] = useState<AIExplainResponse | null>(null)
    const [aiLoading, setAiLoading] = useState(false)
    const [showAi, setShowAi] = useState(false)

    useEffect(() => {
        lessonsApi
            .getById(lessonId, lang)
            .then((r) => {
                setLesson(r.data)
                setCompleted(r.data.is_completed ?? false)
                setQuizPassed(r.data.quiz_passed ?? !r.data.quiz_id)
            })
            .catch(() => router.push(`/learn/${domain}`))
            .finally(() => setLoading(false))
    }, [lessonId, lang, domain, router])

    const handleComplete = async () => {
        try {
            await lessonsApi.complete(lessonId)
            setCompleted(true)
            toast.success('Lesson marked as complete!')
        } catch {
            toast.error('Failed to mark lesson complete')
        }
    }

    const handleAskAI = async () => {
        if (!question.trim()) return
        setAiLoading(true)
        try {
            const res = await lessonsApi.explain(lessonId, { question }, lang)
            setAiResponse(res.data)
        } catch {
            toast.error('AI explain failed. Please try again.')
        } finally {
            setAiLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="max-w-3xl mx-auto space-y-4">
                <div className="h-8 w-64 bg-muted animate-pulse rounded" />
                <div className="h-96 bg-muted animate-pulse rounded-lg" />
            </div>
        )
    }

    if (!lesson) return null

    // Render markdown-ish content (simple newlines + headers)
    const renderContent = (content: string) => {
        return <MarkdownContent content={content} />
    }

    return (
        <div className="max-w-3xl mx-auto space-y-6">
            {/* Back navigation */}
            <div className="flex items-center gap-2">
                <ButtonLink href={`/learn/${domain}`} variant="ghost" size="sm">
                    <ArrowLeft className="h-4 w-4 mr-1" />
                    Back to {domain}
                </ButtonLink>
            </div>

            {/* Header */}
            <div className="space-y-2">
                <div className="flex items-center gap-2">
                    <Badge variant="outline" className="capitalize">{lesson.content_type}</Badge>
                    <span className="flex items-center gap-1 text-xs text-muted-foreground">
                        <Clock className="h-3 w-3" />
                        {lesson.estimated_minutes} min read
                    </span>
                </div>
                <h1 className="text-2xl font-bold">{lesson.title}</h1>
            </div>

            {/* Lesson content */}
            <Card>
                <CardContent className="pt-6">
                    {renderContent(lesson.content)}
                </CardContent>
            </Card>

            {/* AI Explain section */}
            <Card>
                <CardHeader
                    className="cursor-pointer select-none"
                    onClick={() => setShowAi(!showAi)}
                >
                    <CardTitle className="flex items-center justify-between text-base">
                        <span className="flex items-center gap-2">
                            <Lightbulb className="h-4 w-4 text-yellow-400" />
                            Ask AI about this lesson
                        </span>
                        {showAi ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                    </CardTitle>
                </CardHeader>
                {showAi && (
                    <CardContent className="space-y-4">
                        <div className="flex gap-2">
                            <Textarea
                                placeholder="e.g. Can you explain the difference between L4 and L7 load balancers?"
                                value={question}
                                onChange={(e) => setQuestion(e.target.value)}
                                className="min-h-[80px] resize-none"
                            />
                        </div>
                        <Button
                            onClick={handleAskAI}
                            disabled={aiLoading || !question.trim()}
                            size="sm"
                        >
                            <Send className="h-4 w-4 mr-2" />
                            {aiLoading ? 'Asking AI...' : 'Ask AI'}
                        </Button>

                        {aiResponse && (
                            <div className="space-y-4 pt-2 border-t border-border">
                                <div>
                                    <p className="text-sm font-medium mb-1">Explanation</p>
                                    <p className="text-sm text-muted-foreground">{aiResponse.explanation}</p>
                                </div>
                                {aiResponse.key_points.length > 0 && (
                                    <div>
                                        <p className="text-sm font-medium mb-1">Key Points</p>
                                        <ul className="space-y-1">
                                            {aiResponse.key_points.map((pt, i) => (
                                                <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
                                                    <span className="text-primary mt-0.5">•</span>{pt}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                                <div>
                                    <p className="text-sm font-medium mb-1">Real-World Example</p>
                                    <p className="text-sm text-muted-foreground">{aiResponse.real_world_example}</p>
                                </div>
                                <div className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-3">
                                    <p className="text-sm font-medium text-yellow-400 mb-1">Interview Tip</p>
                                    <p className="text-sm text-muted-foreground">{aiResponse.interview_tip}</p>
                                </div>
                            </div>
                        )}
                    </CardContent>
                )}
            </Card>

            {/* Complete button */}
            <div className="flex justify-between items-center gap-3">
                {lesson.quiz_id && (
                    <ButtonLink href={`/learn/${domain}/quiz/${lesson.quiz_id!}?lessonId=${lessonId}`} variant="outline">
                        Take Quiz
                    </ButtonLink>
                )}
                <div className="flex items-center gap-3 ml-auto">
                    {completed ? (
                        <div className="flex items-center gap-3">
                            <div className="flex items-center gap-2 text-green-400 font-medium">
                                <CheckCircle2 className="h-5 w-5" />
                                Lesson completed!
                            </div>
                            {lesson.next_lesson_id && (
                                <ButtonLink href={`/learn/${domain}/lessons/${lesson.next_lesson_id}`}>
                                    Next Lesson
                                    <ArrowRight className="h-4 w-4 ml-2" />
                                </ButtonLink>
                            )}
                        </div>
                    ) : quizPassed ? (
                        <Button onClick={handleComplete} className="gap-2">
                            <CheckCircle2 className="h-4 w-4" />
                            Mark as Complete
                        </Button>
                    ) : (
                        <div className="text-sm text-muted-foreground">
                            Pass the quiz with ≥80% to complete this lesson
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
