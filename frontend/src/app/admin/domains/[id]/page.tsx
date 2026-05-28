'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'
import { adminApi, AdminDomain } from '@/lib/apiClient'

export default function EditDomainPage() {
    const { id } = useParams<{ id: string }>()
    const router = useRouter()
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState('')
    const [form, setForm] = useState<AdminDomain | null>(null)

    useEffect(() => {
        adminApi.getDomains().then((r) => {
            const d = r.data.find((x) => x.id === id)
            if (d) setForm(d)
        })
    }, [id])

    const set = (k: keyof AdminDomain, v: unknown) => setForm((f) => f ? { ...f, [k]: v } : f)

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault()
        if (!form) return
        setError('')
        setSaving(true)
        try {
            await adminApi.updateDomain(id, form)
            router.push('/admin/domains')
        } catch (err: unknown) {
            const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
            setError(msg ?? 'Failed to update domain')
        } finally {
            setSaving(false)
        }
    }

    if (!form) return <p className="text-muted-foreground text-sm">Loading...</p>

    return (
        <div className="max-w-xl">
            <Link href="/admin/domains" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-6">
                <ArrowLeft className="h-4 w-4" /> Domains
            </Link>
            <h1 className="text-2xl font-bold mb-6">Edit Domain</h1>

            {error && <p className="text-sm text-destructive bg-destructive/10 rounded-lg px-3 py-2 mb-4">{error}</p>}

            <form onSubmit={handleSubmit} className="space-y-4">
                <Field label="Slug">
                    <input className="input bg-muted cursor-not-allowed" value={form.slug} disabled />
                </Field>
                <Field label="Name" required>
                    <input className="input" value={form.name} onChange={(e) => set('name', e.target.value)} required />
                </Field>
                <Field label="Description" required>
                    <textarea className="input resize-none h-24" value={form.description} onChange={(e) => set('description', e.target.value)} required />
                </Field>
                <div className="grid grid-cols-2 gap-4">
                    <Field label="Icon name">
                        <input className="input" value={form.icon_name} onChange={(e) => set('icon_name', e.target.value)} />
                    </Field>
                    <Field label="Color">
                        <input className="input" value={form.color} onChange={(e) => set('color', e.target.value)} />
                    </Field>
                </div>
                <Field label="Order index">
                    <input type="number" className="input" value={form.order_index} onChange={(e) => set('order_index', parseInt(e.target.value))} />
                </Field>
                <label className="flex items-center gap-2 text-sm cursor-pointer">
                    <input type="checkbox" checked={form.is_active} onChange={(e) => set('is_active', e.target.checked)} className="h-4 w-4 accent-primary" />
                    Active
                </label>

                <div className="flex gap-3 pt-2">
                    <button type="submit" disabled={saving} className="px-5 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 disabled:opacity-50 transition-colors">
                        {saving ? 'Saving...' : 'Save Changes'}
                    </button>
                    <Link href="/admin/domains" className="px-5 py-2 rounded-lg border border-border text-sm hover:bg-muted transition-colors">
                        Cancel
                    </Link>
                </div>
            </form>
        </div>
    )
}

function Field({ label, required, children }: { label: string; required?: boolean; children: React.ReactNode }) {
    return (
        <div className="space-y-1.5">
            <label className="text-sm font-medium">{label}{required && <span className="text-destructive ml-0.5">*</span>}</label>
            {children}
        </div>
    )
}
