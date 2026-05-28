import Link from 'next/link'
import { MessageSquare, FileText } from 'lucide-react'
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Scenario } from '@/types'

const DIFFICULTY_COLORS = {
    beginner: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    intermediate: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
    advanced: 'bg-red-500/20 text-red-400 border-red-500/30',
}

interface Props {
    scenario: Scenario
}

export function ScenarioCard({ scenario }: Props) {
    const ModeIcon = scenario.mode === 'ai_chat' ? MessageSquare : FileText

    return (
        <Link href={`/scenarios/${scenario.category?.name ?? scenario.category_id}/${scenario.id}`}>
            <Card className="hover:border-primary/50 hover:bg-card/80 transition-colors cursor-pointer h-full">
                <CardHeader>
                    <div className="flex items-start justify-between gap-2">
                        <CardTitle className="text-base leading-snug">{scenario.title}</CardTitle>
                        <ModeIcon className="h-4 w-4 text-muted-foreground mt-0.5 shrink-0" />
                    </div>
                    <CardDescription className="text-sm leading-relaxed">{scenario.description.slice(0, 120)}…</CardDescription>
                    <div className="flex items-center gap-2 pt-1 flex-wrap">
                        <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${DIFFICULTY_COLORS[scenario.difficulty]}`}>
                            {scenario.difficulty}
                        </span>
                        <Badge variant="outline" className="text-xs capitalize">
                            {scenario.mode === 'ai_chat' ? 'AI Chat' : 'Written'}
                        </Badge>
                    </div>
                </CardHeader>
            </Card>
        </Link>
    )
}
