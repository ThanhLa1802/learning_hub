import Link from 'next/link'
import { Calendar, Users, Bug, Code2, Code, Cloud, GitPullRequest } from 'lucide-react'
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ScenarioCategory } from '@/types'

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
    calendar: Calendar,
    users: Users,
    bug: Bug,
    'code-2': Code2,
    code: Code,
    cloud: Cloud,
    'git-pull-request': GitPullRequest,
}

interface Props {
    category: ScenarioCategory
}

export function CategoryCard({ category }: Props) {
    const Icon = ICON_MAP[category.icon_name] ?? Code

    return (
        <Link href={`/scenarios/${category.name}`}>
            <Card className="hover:border-primary/50 hover:bg-card/80 transition-colors cursor-pointer h-full">
                <CardHeader>
                    <div className="flex items-center gap-3">
                        <div className="p-2 rounded-md bg-primary/10 text-primary">
                            <Icon className="h-5 w-5" />
                        </div>
                        <div>
                            <CardTitle className="text-base">{category.title}</CardTitle>
                        </div>
                    </div>
                    <CardDescription className="text-sm leading-relaxed pt-1">{category.description}</CardDescription>
                </CardHeader>
            </Card>
        </Link>
    )
}
