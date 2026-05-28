'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { CheckCircle2, ChevronRight, TrendingUp } from 'lucide-react'
import { sessionsApi } from '@/lib/apiClient'
import { AIFeedback, PracticeSession } from '@/types'
import { Button } from '@/components/ui/button'
import { ButtonLink } from '@/components/ui/button-link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

const SCORE_LABELS: Record<string, string> = {
    grammar_score: 'Grammar',
    vocabulary_score: 'Vocabulary',
    professionalism_score: 'Professionalism',
    it_appropriateness_score: 'IT Appropriateness',
}

function scoreColor(score: number) {
    if (score >= 80) return 'text-emerald-400'
    if (score >= 60) return 'text-amber-400'
    return 'text-red-400'
}

function ScoreRing({ score }: { score: number }) {
    const color = score >= 80 ? '#34d399' : score >= 60 ? '#fbbf24' : '#f87171'
    const radius = 52
    const circumference = 2 * Math.PI * radius
    const dashOffset = circumference - (score / 100) * circumference

    return (
        <div className="relative inline-flex items-center justify-center">
            <svg className="-rotate-90" width="128" height="128">
                <circle cx="64" cy="64" r={radius} fill="none" stroke="currentColor" strokeWidth="8" className="text-muted" />
                <circle
                    cx="64"
                    cy="64"
                    r={radius}
                    fill="none"
                    stroke={color}
                    strokeWidth="8"
                    strokeDasharray={circumference}
                    strokeDashoffset={dashOffset}
                    strokeLinecap="round"
                    className="transition-all duration-700"
                />
            </svg>
            <div className="absolute text-center">
                <span className={`text-3xl font-bold ${scoreColor(score)}`}>{score}</span>
                <p className="text-xs text-muted-foreground -mt-0.5">/ 100</p>
            </div>
        </div>
    )
}

export default function ResultPage() {
    const { sessionId } = useParams<{ sessionId: string }>()
    const [session, setSession] = useState<PracticeSession | null>(null)

    useEffect(() => {
        sessionsApi.getById(sessionId).then((r) => setSession(r.data))
    }, [sessionId])

    if (!session) {
        return (
            <div className="flex justify-center py-20">
                <div className="h-8 w-8 rounded-full border-2 border-primary border-t-transparent animate-spin" />
            </div>
        )
    }

    const feedback = session.ai_feedback as AIFeedback | undefined

    return (
        <div className="max-w-2xl space-y-6">
            <div className="flex items-center gap-3 text-emerald-400">
                <CheckCircle2 className="h-6 w-6" />
                <h1 className="text-xl font-bold">Session Complete!</h1>
            </div>

            <p className="text-muted-foreground">
                <span className="text-foreground font-medium">{session.scenario?.title}</span> ·{' '}
                {session.scenario?.category?.title}
            </p>

            {feedback ? (
                <div className="space-y-6">
                    {/* Overall score */}
                    <Card>
                        <CardContent className="pt-6 flex flex-col items-center gap-4">
                            <ScoreRing score={feedback.overall_score} />
                            <p className="text-sm text-muted-foreground">Overall Score</p>
                        </CardContent>
                    </Card>

                    {/* Sub-scores */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-base flex items-center gap-2">
                                <TrendingUp className="h-4 w-4 text-primary" />
                                Score Breakdown
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            {Object.entries(SCORE_LABELS).map(([key, label]) => {
                                const score = feedback[key as keyof AIFeedback] as number
                                return (
                                    <div key={key} className="space-y-1.5">
                                        <div className="flex justify-between text-sm">
                                            <span>{label}</span>
                                            <span className={`font-medium ${scoreColor(score)}`}>{score}</span>
                                        </div>
                                        <Progress value={score} className="h-1.5" />
                                    </div>
                                )
                            })}
                        </CardContent>
                    </Card>

                    {/* Detailed feedback tabs */}
                    <Tabs defaultValue="strengths">
                        <TabsList className="w-full">
                            <TabsTrigger value="strengths" className="flex-1">Strengths</TabsTrigger>
                            <TabsTrigger value="improvements" className="flex-1">Improvements</TabsTrigger>
                            <TabsTrigger value="examples" className="flex-1">Examples</TabsTrigger>
                        </TabsList>

                        <TabsContent value="strengths" className="mt-3">
                            <Card>
                                <CardContent className="pt-4 space-y-2">
                                    {feedback.strengths.map((s, i) => (
                                        <div key={i} className="flex gap-2 text-sm">
                                            <span className="text-emerald-400 mt-0.5">✓</span>
                                            <span>{s}</span>
                                        </div>
                                    ))}
                                </CardContent>
                            </Card>
                        </TabsContent>

                        <TabsContent value="improvements" className="mt-3">
                            <Card>
                                <CardContent className="pt-4 space-y-2">
                                    {feedback.improvements.map((s, i) => (
                                        <div key={i} className="flex gap-2 text-sm">
                                            <span className="text-amber-400 mt-0.5">→</span>
                                            <span>{s}</span>
                                        </div>
                                    ))}
                                </CardContent>
                            </Card>
                        </TabsContent>

                        <TabsContent value="examples" className="mt-3 space-y-3">
                            {feedback.corrected_example && (
                                <Card>
                                    <CardHeader className="pb-2">
                                        <CardTitle className="text-sm text-amber-400">Corrected Version</CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">{feedback.corrected_example}</p>
                                    </CardContent>
                                </Card>
                            )}
                            {feedback.natural_version && (
                                <Card>
                                    <CardHeader className="pb-2">
                                        <CardTitle className="text-sm text-emerald-400">Native-speaker Version</CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">{feedback.natural_version}</p>
                                    </CardContent>
                                </Card>
                            )}
                        </TabsContent>
                    </Tabs>
                </div>
            ) : (
                <Card>
                    <CardContent className="pt-6 text-center text-muted-foreground">No feedback available.</CardContent>
                </Card>
            )}

            <div className="flex gap-3">
                <ButtonLink href="/history" variant="outline">View History</ButtonLink>
                <ButtonLink href="/dashboard">
                    Practice More
                    <ChevronRight className="h-4 w-4 ml-1" />
                </ButtonLink>
            </div>
        </div>
    )
}
