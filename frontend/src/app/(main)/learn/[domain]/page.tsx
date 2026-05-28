'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import {
    ArrowLeft, BookOpen, Clock, CheckCircle2, ChevronRight,
    MessageSquare, Layers, Globe, Database, Zap, Puzzle,
    Shield, Mail, TableProperties, Gauge, GitMerge, Radio,
    Activity, Split, Triangle
} from 'lucide-react'
import { domainsApi } from '@/services/learnApi'
import { useLang } from '@/contexts/LangContext'
import { DomainWithCourses, LessonSummary } from '@/types/learn'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ButtonLink } from '@/components/ui/button-link'

const ICON_MAP: Record<string, React.ElementType> = {
    'message-square': MessageSquare,
    layers: Layers,
    'book-open': BookOpen,
    globe: Globe,
    database: Database,
    zap: Zap,
    puzzle: Puzzle,
    shield: Shield,
    mail: Mail,
    'table-2': TableProperties,
    gauge: Gauge,
    'git-merge': GitMerge,
    radio: Radio,
    activity: Activity,
    split: Split,
    'triangle-alert': Triangle,
    'git-branch': GitMerge,
}

export default function DomainPage() {
    const params = useParams()
    const router = useRouter()
    const { lang } = useLang()
    const slug = params.domain as string

    const [domain, setDomain] = useState<DomainWithCourses | null>(null)
    const [lessons, setLessons] = useState<LessonSummary[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (!slug) return
        Promise.all([domainsApi.getBySlug(slug, lang), domainsApi.getLessons(slug, undefined, lang)])
            .then(([domainRes, lessonsRes]) => {
                setDomain(domainRes.data)
                setLessons(lessonsRes.data)
            })
            .catch(() => router.push('/learn'))
            .finally(() => setLoading(false))
    }, [slug, lang, router])

    if (loading) {
        return (
            <div className="space-y-4">
                <div className="h-8 w-48 bg-muted animate-pulse rounded" />
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {[1, 2, 3, 4, 5, 6].map((i) => (
                        <div key={i} className="h-32 bg-muted animate-pulse rounded-lg" />
                    ))}
                </div>
            </div>
        )
    }

    if (!domain) return null

    return (
        <div className="space-y-6">
            <div className="flex items-center gap-2">
                <ButtonLink href="/learn" variant="ghost" size="sm">
                    <ArrowLeft className="h-4 w-4 mr-1" />
                    Domains
                </ButtonLink>
            </div>

            <div>
                <h1 className="text-2xl font-bold">{domain.name}</h1>
                <p className="text-muted-foreground mt-1">{domain.description}</p>
                <div className="flex gap-2 mt-3">
                    <Badge variant="secondary">{lessons.length} lessons</Badge>
                    <Badge variant="secondary">{domain.courses.length} course{domain.courses.length !== 1 ? 's' : ''}</Badge>
                </div>
            </div>

            <div>
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold">Lessons</h2>
                    {lessons.some((l) => l.is_completed) && (
                        <span className="text-sm text-muted-foreground">
                            <span className="text-green-400 font-medium">
                                {lessons.filter((l) => l.is_completed).length}
                            </span>
                            /{lessons.length} completed
                        </span>
                    )}
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                    {lessons.map((lesson, index) => {
                        const IconComp = ICON_MAP['book-open']
                        return (
                            <Link key={lesson.id} href={`/learn/${slug}/lessons/${lesson.id}`}>
                                <Card className={`hover:border-primary/50 transition-colors cursor-pointer h-full ${lesson.is_completed ? 'border-green-500/40 bg-green-500/5' : ''}`}>
                                    <CardHeader className="pb-2">
                                        <div className="flex items-center justify-between">
                                            <Badge variant="outline" className="text-xs font-mono">
                                                {String(index + 1).padStart(2, '0')}
                                            </Badge>
                                            <div className="flex items-center gap-2">
                                                {lesson.is_completed && (
                                                    <CheckCircle2 className="h-4 w-4 text-green-400" />
                                                )}
                                                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                                                    <Clock className="h-3 w-3" />
                                                    {lesson.estimated_minutes}m
                                                </div>
                                            </div>
                                        </div>
                                        <CardTitle className="text-sm mt-2 leading-snug">{lesson.title}</CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="flex items-center justify-between">
                                            <Badge variant="secondary" className="text-xs capitalize">
                                                {lesson.content_type}
                                            </Badge>
                                            {lesson.is_completed ? (
                                                <span className="text-xs text-green-400 font-medium">Completed</span>
                                            ) : (
                                                <ChevronRight className="h-4 w-4 text-muted-foreground" />
                                            )}
                                        </div>
                                    </CardContent>
                                </Card>
                            </Link>
                        )
                    })}
                </div>
            </div>
        </div>
    )
}
