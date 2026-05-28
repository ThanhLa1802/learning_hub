'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import {
    BookOpen, Layers, MessageSquare, Globe, Database, Triangle,
    Mail, Shield, Zap, Puzzle, TableProperties, Gauge, GitMerge,
    Radio, Activity, Split, CheckCircle2
} from 'lucide-react'
import { domainsApi, progressApi } from '@/services/learnApi'
import { useLang } from '@/contexts/LangContext'
import { Domain, UserProgress } from '@/types/learn'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'

const ICON_MAP: Record<string, React.ElementType> = {
    'message-square': MessageSquare,
    layers: Layers,
    'book-open': BookOpen,
    globe: Globe,
    database: Database,
}

const COLOR_MAP: Record<string, string> = {
    blue: 'text-blue-400 bg-blue-400/10',
    purple: 'text-purple-400 bg-purple-400/10',
    green: 'text-green-400 bg-green-400/10',
    orange: 'text-orange-400 bg-orange-400/10',
}

export default function LearnPage() {
    const { lang } = useLang()
    const [domains, setDomains] = useState<Domain[]>([])
    const [progress, setProgress] = useState<UserProgress | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        Promise.all([domainsApi.getAll(lang), progressApi.getAll()])
            .then(([domainsRes, progressRes]) => {
                setDomains(domainsRes.data)
                setProgress(progressRes.data)
            })
            .finally(() => setLoading(false))
    }, [lang])

    if (loading) {
        return (
            <div className="space-y-4">
                {[1, 2].map((i) => (
                    <div key={i} className="h-40 rounded-lg bg-muted animate-pulse" />
                ))}
            </div>
        )
    }

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl font-bold">Learning Domains</h1>
                <p className="text-muted-foreground mt-1">
                    Choose a domain to start learning. Each domain has structured lessons, quizzes, and AI practice scenarios.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {domains.map((domain) => {
                    const IconComp = ICON_MAP[domain.icon_name] ?? BookOpen
                    const colorClass = COLOR_MAP[domain.color] ?? 'text-primary bg-primary/10'
                    const domainProgress = progress?.domains.find((d) => d.domain_id === domain.id)

                    return (
                        <Link key={domain.id} href={`/learn/${domain.slug}`}>
                            <Card className="hover:border-primary/50 transition-colors cursor-pointer h-full">
                                <CardHeader className="pb-3">
                                    <div className="flex items-start gap-4">
                                        <div className={`p-3 rounded-lg ${colorClass}`}>
                                            <IconComp className="h-6 w-6" />
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <CardTitle className="text-lg">{domain.name}</CardTitle>
                                            <CardDescription className="mt-1 line-clamp-2">
                                                {domain.description}
                                            </CardDescription>
                                        </div>
                                    </div>
                                </CardHeader>
                                <CardContent>
                                    {domainProgress && domainProgress.lessons_completed > 0 ? (
                                        <div className="space-y-2">
                                            <div className="flex items-center justify-between text-sm">
                                                {domainProgress.total_lessons > 0 && domainProgress.lessons_completed >= domainProgress.total_lessons ? (
                                                    <span className="flex items-center gap-1.5 text-green-400 font-medium text-xs">
                                                        <CheckCircle2 className="h-4 w-4" />
                                                        All {domainProgress.total_lessons} lessons completed
                                                    </span>
                                                ) : (
                                                    <>
                                                        <span className="text-muted-foreground">Progress</span>
                                                        <div className="flex gap-3 text-xs">
                                                            <span>
                                                                <span className="font-medium text-foreground">{domainProgress.lessons_completed}</span>/{domainProgress.total_lessons} lessons
                                                            </span>
                                                            <span>
                                                                <span className="font-medium text-foreground">{domainProgress.quizzes_taken}</span> quizzes
                                                            </span>
                                                            {domainProgress.avg_quiz_score > 0 && (
                                                                <span>
                                                                    <span className="font-medium text-foreground">{Math.round(domainProgress.avg_quiz_score)}%</span> avg
                                                                </span>
                                                            )}
                                                        </div>
                                                    </>
                                                )}
                                            </div>
                                        </div>
                                    ) : (
                                        <Badge variant="secondary" className="text-xs">Not started</Badge>
                                    )}
                                </CardContent>
                            </Card>
                        </Link>
                    )
                })}
            </div>
        </div>
    )
}
