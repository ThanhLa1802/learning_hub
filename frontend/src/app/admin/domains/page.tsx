'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { PlusCircle, Pencil, CheckCircle, XCircle } from 'lucide-react'
import { adminApi, AdminDomain } from '@/lib/apiClient'

export default function DomainsPage() {
    const [domains, setDomains] = useState<AdminDomain[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        adminApi.getDomains()
            .then((r) => setDomains(r.data))
            .finally(() => setLoading(false))
    }, [])

    return (
        <div>
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-2xl font-bold">Domains</h1>
                <Link
                    href="/admin/domains/new"
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors"
                >
                    <PlusCircle className="h-4 w-4" /> New Domain
                </Link>
            </div>

            {loading ? (
                <p className="text-muted-foreground text-sm">Loading...</p>
            ) : (
                <div className="border border-border rounded-xl overflow-hidden">
                    <table className="w-full text-sm">
                        <thead className="bg-muted text-muted-foreground">
                            <tr>
                                <th className="text-left px-4 py-3 font-medium">Name</th>
                                <th className="text-left px-4 py-3 font-medium">Slug</th>
                                <th className="text-left px-4 py-3 font-medium">Order</th>
                                <th className="text-left px-4 py-3 font-medium">Active</th>
                                <th className="px-4 py-3" />
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border">
                            {domains.map((d) => (
                                <tr key={d.id} className="hover:bg-muted/40 transition-colors">
                                    <td className="px-4 py-3 font-medium">{d.name}</td>
                                    <td className="px-4 py-3 text-muted-foreground font-mono">{d.slug}</td>
                                    <td className="px-4 py-3 text-muted-foreground">{d.order_index}</td>
                                    <td className="px-4 py-3">
                                        {d.is_active
                                            ? <CheckCircle className="h-4 w-4 text-green-500" />
                                            : <XCircle className="h-4 w-4 text-muted-foreground" />}
                                    </td>
                                    <td className="px-4 py-3 text-right">
                                        <Link
                                            href={`/admin/domains/${d.id}`}
                                            className="inline-flex items-center gap-1 text-xs text-primary hover:underline"
                                        >
                                            <Pencil className="h-3 w-3" /> Edit
                                        </Link>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    )
}
