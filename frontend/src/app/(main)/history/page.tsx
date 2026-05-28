'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { History, TrendingUp, ChevronRight } from 'lucide-react'
import { sessionsApi } from '@/lib/apiClient'
import { PracticeSession } from '@/types'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { ButtonLink } from '@/components/ui/button-link'

const DIFFICULTY_COLORS = {
    beginner: 'text-emerald-400',
    intermediate: 'text-amber-400',
    advanced: 'text-red-400',
}

export default function HistoryPage() {
    const [sessions, setSessions] = useState<PracticeSession[]>([])
    const [total, setTotal] = useState(0)
    const [skip, setSkip] = useState(0)
    const limit = 10

    const fetchSessions = async (s: number) => {
        const res = await sessionsApi.list(s, limit)
        setSessions(res.data.items)
        setTotal(res.data.total)
        setSkip(s)
    }

    useEffect(() => {
        fetchSessions(0)
    }, [])

    return (
        <div className="space-y-6">
            <div className="flex items-center gap-2">
                <History className="h-5 w-5 text-primary" />
                <h1 className="text-xl font-bold">Practice History</h1>
                <Badge variant="secondary" className="ml-1">{total} sessions</Badge>
            </div>

            {sessions.length === 0 ? (
                <div className="text-center py-16 space-y-3">
                    <p className="text-muted-foreground">No sessions yet.</p>
                    <ButtonLink href="/dashboard">Start Practising</ButtonLink>
                </div>
            ) : (
                <div className="space-y-2">
                    {sessions.map((s) => (
                        <SessionRow key={s.id} session={s} />
                    ))}
                </div>
            )}

            {total > limit && (
                <div className="flex justify-center gap-3">
                    <Button variant="outline" size="sm" disabled={skip === 0} onClick={() => fetchSessions(skip - limit)}>
                        Previous
                    </Button>
                    <span className="text-sm text-muted-foreground self-center">
                        {Math.floor(skip / limit) + 1} / {Math.ceil(total / limit)}
                    </span>
                    <Button variant="outline" size="sm" disabled={skip + limit >= total} onClick={() => fetchSessions(skip + limit)}>
                        Next
                    </Button>
                </div>
            )}
        </div>
    )
}

function SessionRow({ session }: { session: PracticeSession }) {
    const href = session.status === 'completed' ? `/practice/${session.id}/result` : `/practice/${session.id}`
    const diff = session.scenario?.difficulty

    return (
        <Link href={href}>
            <Card className="hover:border-primary/30 transition-colors cursor-pointer">
                <CardContent className="py-3 px-4">
                    <div className="flex items-center gap-4">
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium truncate">{session.scenario?.title ?? 'Session'}</p>
                            <div className="flex items-center gap-2 mt-0.5">
                                <span className="text-xs text-muted-foreground">{session.scenario?.category?.title}</span>
                                {diff && (
                                    <span className={`text-xs font-medium ${DIFFICULTY_COLORS[diff]}`}>· {diff}</span>
                                )}
                            </div>
                        </div>
                        <div className="flex items-center gap-3 shrink-0">
                            {session.overall_score != null && (
                                <div className="flex items-center gap-1 text-sm font-semibold">
                                    <TrendingUp className="h-3.5 w-3.5 text-primary" />
                                    {session.overall_score}
                                </div>
                            )}
                            <Badge variant={session.status === 'completed' ? 'default' : 'secondary'} className="text-xs capitalize">
                                {session.status.replace('_', ' ')}
                            </Badge>
                            <ChevronRight className="h-4 w-4 text-muted-foreground" />
                        </div>
                    </div>
                </CardContent>
            </Card>
        </Link>
    )
}
