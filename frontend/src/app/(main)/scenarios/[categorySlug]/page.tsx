'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'
import { scenariosApi } from '@/lib/apiClient'
import { Scenario, ScenarioCategory } from '@/types'
import { ScenarioCard } from '@/components/scenarios/ScenarioCard'
import { Button } from '@/components/ui/button'
import { ButtonLink } from '@/components/ui/button-link'

export default function CategoryPage() {
    const { categorySlug } = useParams<{ categorySlug: string }>()
    const [scenarios, setScenarios] = useState<Scenario[]>([])
    const [category, setCategory] = useState<ScenarioCategory | null>(null)

    useEffect(() => {
        scenariosApi.getCategories().then((r) => {
            const cat = r.data.find((c) => c.name === categorySlug)
            if (cat) {
                setCategory(cat)
                scenariosApi.getAll({ category_id: cat.id }).then((s) => setScenarios(s.data))
            }
        })
    }, [categorySlug])

    return (
        <div className="space-y-6">
            <div className="flex items-center gap-3">
                <ButtonLink href="/dashboard" variant="ghost" size="sm">
                    <ArrowLeft className="h-4 w-4 mr-1" />
                    Back
                </ButtonLink>
            </div>

            {category && (
                <div>
                    <h1 className="text-2xl font-bold">{category.title}</h1>
                    <p className="text-muted-foreground mt-1">{category.description}</p>
                </div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {scenarios.map((s) => (
                    <ScenarioCard key={s.id} scenario={s} />
                ))}
            </div>
        </div>
    )
}
