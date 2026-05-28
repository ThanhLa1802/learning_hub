'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Clock, TrendingUp, BookOpen, GraduationCap, ArrowRight, ChevronDown, ChevronUp } from 'lucide-react'
import { scenariosApi, sessionsApi } from '@/lib/apiClient'
import { domainsApi } from '@/services/learnApi'
import { useAuth } from '@/hooks/useAuth'
import { ScenarioCategory, PracticeSession } from '@/types'
import { DomainWithCourses } from '@/types/learn'
import { CategoryCard } from '@/components/scenarios/CategoryCard'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ButtonLink } from '@/components/ui/button-link'

export default function DashboardPage() {
    const { user } = useAuth()
    const [categories, setCategories] = useState<ScenarioCategory[]>([])
    const [domains, setDomains] = useState<DomainWithCourses[]>([])
    const [recentSessions, setRecentSessions] = useState<PracticeSession[]>([])
    const [expandedDomains, setExpandedDomains] = useState<Set<string>>(new Set())

    useEffect(() => {
        scenariosApi.getCategories().then((r) => setCategories(r.data))
        domainsApi.getAll().then((r) => setDomains(r.data))
        sessionsApi.list(0, 5).then((r) => {
            // deduplicate by id
            const seen = new Set<string>()
            const unique = r.data.items.filter((s) => {
                if (seen.has(s.id)) return false
                seen.add(s.id)
                return true
            })
            setRecentSessions(unique)
        })
    }, [])

    const toggleDomain = (slug: string) => {
        setExpandedDomains((prev) => {
            const next = new Set(prev)
            next.has(slug) ? next.delete(slug) : next.add(slug)
            return next
        })
    }

    const INITIAL_VISIBLE = 4

    // Build a map: courseId → domain
    const courseToDomainsMap = new Map<string, DomainWithCourses>()
    domains.forEach((d) => d.courses.forEach((c) => courseToDomainsMap.set(c.id, d)))

    // Group categories by domain slug; uncategorized goes to "other"
    const grouped = new Map<string, { domain: DomainWithCourses; cats: ScenarioCategory[] }>()
    const ungrouped: ScenarioCategory[] = []
    categories.forEach((cat) => {
        if (cat.course_id) {
            const domain = courseToDomainsMap.get(cat.course_id)
            if (domain) {
                if (!grouped.has(domain.slug)) grouped.set(domain.slug, { domain, cats: [] })
                grouped.get(domain.slug)!.cats.push(cat)
                return
            }
        }
        ungrouped.push(cat)
    })

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl font-bold">Welcome back, {user?.full_name.split(' ')[0]} 👋</h1>
                <p className="text-muted-foreground mt-1">Practice English or study structured system design content.</p>
            </div>

            {/* Learn CTA */}
            <Card className="border-purple-500/30 bg-purple-500/5">
                <CardContent className="py-5 px-6">
                    <div className="flex items-center justify-between gap-4">
                        <div className="flex items-center gap-4">
                            <div className="p-3 rounded-lg bg-purple-500/10 text-purple-400">
                                <GraduationCap className="h-6 w-6" />
                            </div>
                            <div>
                                <p className="font-semibold">Learning Domains</p>
                                <p className="text-sm text-muted-foreground">
                                    Structured lessons + quizzes for System Design and IT English.
                                </p>
                            </div>
                        </div>
                        <ButtonLink href="/learn" variant="outline" size="sm" className="shrink-0 border-purple-500/30 hover:border-purple-500/60">
                            Explore
                            <ArrowRight className="h-4 w-4 ml-1" />
                        </ButtonLink>
                    </div>
                </CardContent>
            </Card>

            <section>
                <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                    <BookOpen className="h-5 w-5 text-primary" />
                    Practice Categories
                </h2>
                <div className="space-y-6">
                    {Array.from(grouped.values()).map(({ domain, cats }) => {
                        const isExpanded = expandedDomains.has(domain.slug)
                        const visible = isExpanded ? cats : cats.slice(0, INITIAL_VISIBLE)
                        const hidden = cats.length - INITIAL_VISIBLE
                        return (
                            <div key={domain.slug}>
                                <div className="flex items-center gap-2 mb-3">
                                    <span className="text-sm font-medium text-muted-foreground uppercase tracking-wide">
                                        {domain.name}
                                    </span>
                                    <div className="flex-1 h-px bg-border" />
                                </div>
                                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                                    {visible.map((c) => (
                                        <CategoryCard key={c.id} category={c} />
                                    ))}
                                </div>
                                {cats.length > INITIAL_VISIBLE && (
                                    <button
                                        onClick={() => toggleDomain(domain.slug)}
                                        className="mt-3 flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors"
                                    >
                                        {isExpanded ? (
                                            <><ChevronUp className="h-4 w-4" /> Show less</>
                                        ) : (
                                            <><ChevronDown className="h-4 w-4" /> View {hidden} more</>
                                        )}
                                    </button>
                                )}
                            </div>
                        )
                    })}
                    {ungrouped.length > 0 && (
                        <div>
                            <div className="flex items-center gap-2 mb-3">
                                <span className="text-sm font-medium text-muted-foreground uppercase tracking-wide">General</span>
                                <div className="flex-1 h-px bg-border" />
                            </div>
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                                {ungrouped.map((c) => (
                                    <CategoryCard key={c.id} category={c} />
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </section>

            {recentSessions.length > 0 && (
                <section>
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-lg font-semibold flex items-center gap-2">
                            <Clock className="h-5 w-5 text-primary" />
                            Recent Sessions
                        </h2>
                        <Link href="/history" className="text-sm text-primary hover:underline">
                            View all →
                        </Link>
                    </div>
                    <div className="space-y-2">
                        {recentSessions.map((s) => (
                            <RecentSessionRow key={s.id} session={s} />
                        ))}
                    </div>
                </section>
            )}
        </div>
    )
}

function RecentSessionRow({ session }: { session: PracticeSession }) {
    return (
        <Link href={session.status === 'completed' ? `/practice/${session.id}/result` : `/practice/${session.id}`}>
            <Card className="hover:border-primary/30 transition-colors cursor-pointer">
                <CardContent className="py-3 px-4">
                    <div className="flex items-center justify-between gap-4">
                        <div className="min-w-0">
                            <p className="text-sm font-medium truncate">{session.scenario?.title ?? 'Practice Session'}</p>
                            <p className="text-xs text-muted-foreground">{session.scenario?.category?.title}</p>
                        </div>
                        <div className="flex items-center gap-2 shrink-0">
                            {session.overall_score != null && (
                                <div className="flex items-center gap-1 text-sm font-semibold">
                                    <TrendingUp className="h-3.5 w-3.5 text-primary" />
                                    {session.overall_score}
                                </div>
                            )}
                            <Badge variant={session.status === 'completed' ? 'default' : 'secondary'} className="text-xs capitalize">
                                {session.status.replace('_', ' ')}
                            </Badge>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </Link>
    )
}
