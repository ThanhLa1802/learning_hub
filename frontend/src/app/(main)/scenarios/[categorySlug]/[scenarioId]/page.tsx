'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft, MessageSquare, FileText, Zap } from 'lucide-react'
import { scenariosApi, sessionsApi } from '@/lib/apiClient'
import { Scenario } from '@/types'
import { Button } from '@/components/ui/button'
import { ButtonLink } from '@/components/ui/button-link'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { toast } from 'sonner'

const DIFFICULTY_COLORS = {
    beginner: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    intermediate: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
    advanced: 'bg-red-500/20 text-red-400 border-red-500/30',
}

export default function ScenarioDetailPage() {
    const { scenarioId } = useParams<{ scenarioId: string }>()
    const router = useRouter()
    const [scenario, setScenario] = useState<Scenario | null>(null)
    const [starting, setStarting] = useState(false)

    useEffect(() => {
        scenariosApi.getById(scenarioId).then((r) => setScenario(r.data))
    }, [scenarioId])

    const handleStart = async () => {
        if (!scenario) return
        setStarting(true)
        try {
            const res = await sessionsApi.create({ scenario_id: scenario.id })
            router.push(`/practice/${res.data.id}`)
        } catch {
            toast.error('Failed to start session')
            setStarting(false)
        }
    }

    if (!scenario) return <div className="flex justify-center py-20"><div className="h-8 w-8 rounded-full border-2 border-primary border-t-transparent animate-spin" /></div>

    const ModeIcon = scenario.mode === 'ai_chat' ? MessageSquare : FileText

    return (
        <div className="max-w-2xl space-y-6">
            <ButtonLink href={`/scenarios/${scenario.category?.name}`} variant="ghost" size="sm">
                <ArrowLeft className="h-4 w-4 mr-1" />
                {scenario.category?.title ?? 'Back'}
            </ButtonLink>

            <div>
                <div className="flex items-start gap-3 mb-3">
                    <h1 className="text-2xl font-bold">{scenario.title}</h1>
                </div>
                <div className="flex items-center gap-2 flex-wrap">
                    <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${DIFFICULTY_COLORS[scenario.difficulty]}`}>
                        {scenario.difficulty}
                    </span>
                    <Badge variant="outline" className="text-xs gap-1">
                        <ModeIcon className="h-3 w-3" />
                        {scenario.mode === 'ai_chat' ? 'AI Roleplay Chat' : 'Written Response'}
                    </Badge>
                    {scenario.tags.map((tag) => (
                        <Badge key={tag} variant="secondary" className="text-xs">{tag}</Badge>
                    ))}
                </div>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle className="text-base">Scenario</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-muted-foreground leading-relaxed">{scenario.description}</p>
                </CardContent>
            </Card>

            <Card className="border-primary/20 bg-primary/5">
                <CardContent className="pt-4">
                    <div className="flex items-start gap-3">
                        <ModeIcon className="h-5 w-5 text-primary mt-0.5" />
                        <div>
                            <p className="font-medium text-sm">
                                {scenario.mode === 'ai_chat' ? 'AI Roleplay Chat' : 'Written Response + AI Evaluation'}
                            </p>
                            <p className="text-xs text-muted-foreground mt-1">
                                {scenario.mode === 'ai_chat'
                                    ? 'You will have a real conversation with an AI playing a specific role. When you are done, end the session to receive an evaluation of your English.'
                                    : 'Write your response to the scenario above. Our AI will evaluate your grammar, vocabulary, professionalism, and technical communication.'}
                            </p>
                        </div>
                    </div>
                </CardContent>
            </Card>

            <Button size="lg" onClick={handleStart} disabled={starting} className="gap-2">
                <Zap className="h-4 w-4" />
                {starting ? 'Starting…' : 'Start Practice'}
            </Button>
        </div>
    )
}
