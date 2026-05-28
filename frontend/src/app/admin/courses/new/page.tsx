'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'
import { adminApi, AdminDomain } from '@/lib/apiClient'

export default function NewCoursePage() {
    const router = useRouter()
    const [domains, setDomains] = useState<AdminDomain[]>([])
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState('')
    const [form, setForm] = useState({
        domain_id: '', slug: '', name: '', description: '', order_index: 0, is_active: true,
    })

    useEffect(() => {
        adminApi.getDomains().then((r) => {
            setDomains(r.data)
            if (r.data.length > 0) setForm((f) => ({ ...f, domain_id: r.data[0].id }))
        })
    }, [])

    const set = (k: keyof typeof form, v: unknown) => setForm((f) => ({ ...f, [k]: v }))

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault()
        setError('')
        setSaving(true)
        try {
            await adminApi.createCourse(form)
            router.push('/admin/courses')
        } catch (err: unknown) {
            const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
            setError(msg ?? 'Failed to create course')
        } finally {
            setSaving(false)
        }
    }

    return (
        <div className="max-w-xl">
            <Link href="/admin/courses" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-6">
                <ArrowLeft className="h-4 w-4" /> Courses
            </Link>
            <h1 className="text-2xl font-bold mb-6">New Course</h1>

            {error && <p className="text-sm text-destructive bg-destructive/10 rounded-lg px-3 py-2 mb-4">{error}</p>}

            <form onSubmit={handleSubmit} className="space-y-4">
                <Field label="Domain" required>
                    <select className="input" value={form.domain_id} onChange={(e) => set('domain_id', e.target.value)} required>
                        {domains.map((d) => <option key={d.id} value={d.id}>{d.name}</option>)}
                    </select>
                </Field>
                <Field label="Slug" required>
                    <input className="input" value={form.slug} onChange={(e) => set('slug', e.target.value)} placeholder="e.g. go-basics" required />
                </Field>
                <Field label="Name" required>
                    <input className="input" value={form.name} onChange={(e) => set('name', e.target.value)} placeholder="e.g. Go Basics" required />
                </Field>
                <Field label="Description" required>
                    <textarea className="input resize-none h-24" value={form.description} onChange={(e) => set('description', e.target.value)} required />
                </Field>
                <Field label="Order index">
                    <input type="number" className="input" value={form.order_index} onChange={(e) => set('order_index', parseInt(e.target.value))} />
                </Field>
                <label className="flex items-center gap-2 text-sm cursor-pointer">
                    <input type="checkbox" checked={form.is_active} onChange={(e) => set('is_active', e.target.checked)} className="h-4 w-4 accent-primary" />
                    Active
                </label>

                <div className="flex gap-3 pt-2">
                    <button type="submit" disabled={saving} className="px-5 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 disabled:opacity-50 transition-colors">
                        {saving ? 'Saving...' : 'Create Course'}
                    </button>
                    <Link href="/admin/courses" className="px-5 py-2 rounded-lg border border-border text-sm hover:bg-muted transition-colors">
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
