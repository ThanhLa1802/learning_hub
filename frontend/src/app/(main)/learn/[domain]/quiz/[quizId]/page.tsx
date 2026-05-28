'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft, CheckCircle2, XCircle, Trophy, RotateCcw } from 'lucide-react'
import { quizzesApi } from '@/services/learnApi'
import { useLang } from '@/contexts/LangContext'
import { Quiz, QuizAttemptResult } from '@/types/learn'
import { Button } from '@/components/ui/button'
import { ButtonLink } from '@/components/ui/button-link'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { toast } from 'sonner'

export default function QuizPage() {
    const params = useParams()
    const router = useRouter()
    const { lang } = useLang()
    const domain = params.domain as string
    const quizId = params.quizId as string
    const searchParams = useSearchParams()
    const lessonId = searchParams.get('lessonId')

    const [quiz, setQuiz] = useState<Quiz | null>(null)
    const [loading, setLoading] = useState(true)
    const [answers, setAnswers] = useState<(number | null)[]>([])
    const [submitting, setSubmitting] = useState(false)
    const [result, setResult] = useState<QuizAttemptResult | null>(null)

    useEffect(() => {
        quizzesApi
            .getById(quizId, lang)
            .then((r) => {
                setQuiz(r.data)
                setAnswers(new Array(r.data.questions.length).fill(null))
            })
            .catch(() => router.push(`/learn/${domain}`))
            .finally(() => setLoading(false))
    }, [quizId, lang, domain, router])

    const handleSelect = (questionIndex: number, optionIndex: number) => {
        if (result) return // locked after submission
        setAnswers((prev) => {
            const next = [...prev]
            next[questionIndex] = optionIndex
            return next
        })
    }

    const handleSubmit = async () => {
        if (!quiz) return
        const unanswered = answers.findIndex((a) => a === null)
        if (unanswered !== -1) {
            toast.error(`Please answer question ${unanswered + 1} before submitting.`)
            return
        }

        setSubmitting(true)
        try {
            const res = await quizzesApi.submit(quizId, answers as number[])
            setResult(res.data)
        } catch {
            toast.error('Failed to submit quiz. Please try again.')
        } finally {
            setSubmitting(false)
        }
    }

    const handleRetry = () => {
        setResult(null)
        setAnswers(new Array(quiz?.questions.length ?? 0).fill(null))
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    if (loading) {
        return (
            <div className="max-w-2xl mx-auto space-y-4">
                <div className="h-8 w-64 bg-muted animate-pulse rounded" />
                {[1, 2, 3].map((i) => (
                    <div key={i} className="h-40 bg-muted animate-pulse rounded-lg" />
                ))}
            </div>
        )
    }

    if (!quiz) return null

    const scorePercent = result ? Math.round(result.score) : 0

    return (
        <div className="max-w-2xl mx-auto space-y-6">
            {/* Back nav */}
            <div className="flex items-center gap-2">
                <ButtonLink href={`/learn/${domain}`} variant="ghost" size="sm">
                    <ArrowLeft className="h-4 w-4 mr-1" />
                    Back to {domain}
                </ButtonLink>
            </div>

            {/* Header */}
            <div>
                <h1 className="text-2xl font-bold">{quiz.title}</h1>
                {quiz.description && (
                    <p className="text-muted-foreground mt-1">{quiz.description}</p>
                )}
                <div className="flex items-center gap-3 mt-3">
                    <Badge variant="secondary">{quiz.questions.length} questions</Badge>
                    {!result && (
                        <span className="text-sm text-muted-foreground">
                            {answers.filter((a) => a !== null).length} / {quiz.questions.length} answered
                        </span>
                    )}
                </div>
                {!result && (
                    <Progress
                        value={(answers.filter((a) => a !== null).length / quiz.questions.length) * 100}
                        className="mt-3 h-1.5"
                    />
                )}
            </div>

            {/* Result summary */}
            {result && (
                <Card className={scorePercent >= 80 ? 'border-green-500/40 bg-green-500/5' : scorePercent >= 60 ? 'border-yellow-500/40 bg-yellow-500/5' : 'border-red-500/40 bg-red-500/5'}>
                    <CardContent className="pt-6 text-center space-y-3">
                        <Trophy className={`h-10 w-10 mx-auto ${scorePercent >= 80 ? 'text-green-400' : scorePercent >= 60 ? 'text-yellow-400' : 'text-red-400'}`} />
                        <div>
                            <p className="text-3xl font-bold">{scorePercent}%</p>
                            <p className="text-muted-foreground text-sm">{result.feedback}</p>
                        </div>
                        {scorePercent < 80 && (
                            <p className="text-sm text-yellow-400 font-medium">
                                You need ≥80% to pass. Give it another try!
                            </p>
                        )}
                        <div className="flex justify-center gap-3 mt-2 text-sm">
                            <span className="text-green-400">
                                ✓ {result.results.filter((r) => r.is_correct).length} correct
                            </span>
                            <span className="text-red-400">
                                ✗ {result.results.filter((r) => !r.is_correct).length} incorrect
                            </span>
                        </div>
                        <div className="flex justify-center gap-3 pt-2">
                            <Button variant="outline" size="sm" onClick={handleRetry}>
                                <RotateCcw className="h-4 w-4 mr-1" />
                                Try Again
                            </Button>
                            {scorePercent >= 80 && lessonId && (
                                <ButtonLink
                                    href={`/learn/${domain}/lessons/${lessonId}`}
                                    size="sm"
                                >
                                    <CheckCircle2 className="h-4 w-4 mr-1" />
                                    Back to Lesson
                                </ButtonLink>
                            )}
                            {scorePercent >= 80 && !lessonId && (
                                <ButtonLink href={`/learn/${domain}`} size="sm">
                                    Continue Learning
                                </ButtonLink>
                            )}
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Questions */}
            <div className="space-y-6">
                {quiz.questions.map((question, qi) => {
                    const qResult = result?.results[qi]
                    const selected = answers[qi]

                    return (
                        <Card key={question.id}>
                            <CardHeader className="pb-3">
                                <div className="flex items-start gap-3">
                                    {result && (
                                        qResult?.is_correct
                                            ? <CheckCircle2 className="h-5 w-5 text-green-400 mt-0.5 shrink-0" />
                                            : <XCircle className="h-5 w-5 text-red-400 mt-0.5 shrink-0" />
                                    )}
                                    <CardTitle className="text-sm font-medium leading-snug">
                                        <span className="text-muted-foreground mr-2">Q{qi + 1}.</span>
                                        {question.question}
                                    </CardTitle>
                                </div>
                            </CardHeader>
                            <CardContent className="space-y-2">
                                {question.options.map((option, oi) => {
                                    let variant: 'default' | 'correct' | 'incorrect' | 'neutral' = 'neutral'
                                    if (result && qResult) {
                                        if (oi === qResult.correct_answer_index) variant = 'correct'
                                        else if (oi === selected && !qResult.is_correct) variant = 'incorrect'
                                    } else if (selected === oi) {
                                        variant = 'default'
                                    }

                                    const baseClass = 'w-full text-left px-4 py-3 rounded-lg border text-sm transition-colors'
                                    const variantClass =
                                        variant === 'correct' ? 'border-green-500 bg-green-500/10 text-green-300' :
                                            variant === 'incorrect' ? 'border-red-500 bg-red-500/10 text-red-300' :
                                                variant === 'default' ? 'border-primary bg-primary/10 text-primary' :
                                                    'border-border hover:border-muted-foreground hover:bg-muted/50 cursor-pointer'

                                    return (
                                        <button
                                            key={oi}
                                            className={`${baseClass} ${variantClass}`}
                                            onClick={() => handleSelect(qi, oi)}
                                            disabled={!!result}
                                        >
                                            <span className="font-mono mr-2 text-xs opacity-70">
                                                {String.fromCharCode(65 + oi)}.
                                            </span>
                                            {option}
                                        </button>
                                    )
                                })}

                                {result && qResult && (
                                    <div className="mt-2 pt-2 border-t border-border">
                                        <p className="text-xs text-muted-foreground">
                                            <span className="font-medium text-foreground">Explanation: </span>
                                            {qResult.explanation}
                                        </p>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    )
                })}
            </div>

            {/* Submit */}
            {!result && (
                <div className="flex justify-end">
                    <Button
                        onClick={handleSubmit}
                        disabled={submitting || answers.some((a) => a === null)}
                        size="lg"
                    >
                        {submitting ? 'Submitting...' : 'Submit Quiz'}
                    </Button>
                </div>
            )}
        </div>
    )
}
