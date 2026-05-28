'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft, Eye, Code } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { adminApi } from '@/lib/apiClient'

const CONTENT_TYPES = ['explanation', 'practice', 'example', 'exercise', 'quiz']

interface LessonForm {
    title: string
    content: string
    content_type: string
    order_index: number
    estimated_minutes: number
    is_active: boolean
}

export default function EditLessonPage() {
    const { id } = useParams<{ id: string }>()
    const router = useRouter()
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState('')
    const [preview, setPreview] = useState(false)
    const [meta, setMeta] = useState({ course_name: '', domain_name: '' })
    const [form, setForm] = useState<LessonForm | null>(null)

    useEffect(() => {
        adminApi.getLessonDetail(id).then((r) => {
            const { title, content, content_type, order_index, estimated_minutes, is_active, course_name, domain_name } = r.data
            setMeta({ course_name, domain_name })
            setForm({ title, content, content_type, order_index, estimated_minutes, is_active })
        })
    }, [id])

    const set = (k: keyof LessonForm, v: unknown) => setForm((f) => f ? { ...f, [k]: v } : f)

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault()
        if (!form) return
        setError('')
        setSaving(true)
        try {
            await adminApi.updateLesson(id, form)
            router.push('/admin/lessons')
        } catch (err: unknown) {
            const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
            setError(msg ?? 'Failed to update lesson')
        } finally {
            setSaving(false)
        }
    }

    if (!form) return <p className="text-muted-foreground text-sm">Loading...</p>

    return (
        <div>
            <Link href="/admin/lessons" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-6">
                <ArrowLeft className="h-4 w-4" /> Lessons
            </Link>
            <h1 className="text-2xl font-bold mb-1">Edit Lesson</h1>
            <p className="text-sm text-muted-foreground mb-6">{meta.domain_name} › {meta.course_name}</p>

            {error && <p className="text-sm text-destructive bg-destructive/10 rounded-lg px-3 py-2 mb-4">{error}</p>}

            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                    <Field label="Content type">
                        <select className="input" value={form.content_type} onChange={(e) => set('content_type', e.target.value)}>
                            {CONTENT_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
                        </select>
                    </Field>
                </div>

                <Field label="Title" required>
                    <input className="input" value={form.title} onChange={(e) => set('title', e.target.value)} required />
                </Field>

                <div className="grid grid-cols-2 gap-4">
                    <Field label="Order index">
                        <input type="number" className="input" value={form.order_index} onChange={(e) => set('order_index', parseInt(e.target.value))} />
                    </Field>
                    <Field label="Estimated minutes">
                        <input type="number" className="input" value={form.estimated_minutes} onChange={(e) => set('estimated_minutes', parseInt(e.target.value))} />
                    </Field>
                </div>

                <label className="flex items-center gap-2 text-sm cursor-pointer">
                    <input type="checkbox" checked={form.is_active} onChange={(e) => set('is_active', e.target.checked)} className="h-4 w-4 accent-primary" />
                    Active
                </label>

                <Field label="Content (Markdown)" required>
                    <div className="border border-border rounded-xl overflow-hidden">
                        <div className="flex border-b border-border bg-muted px-3 py-1.5 gap-2">
                            <button type="button" onClick={() => setPreview(false)}
                                className={`flex items-center gap-1.5 text-xs px-2 py-1 rounded ${!preview ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground'}`}>
                                <Code className="h-3 w-3" /> Write
                            </button>
                            <button type="button" onClick={() => setPreview(true)}
                                className={`flex items-center gap-1.5 text-xs px-2 py-1 rounded ${preview ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground'}`}>
                                <Eye className="h-3 w-3" /> Preview
                            </button>
                        </div>
                        {!preview ? (
                            <textarea
                                className="w-full bg-background p-3 text-sm font-mono resize-none focus:outline-none min-h-[400px]"
                                value={form.content}
                                onChange={(e) => set('content', e.target.value)}
                                required
                            />
                        ) : (
                            <div className="prose prose-sm dark:prose-invert max-w-none p-4 min-h-[400px]">
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>{form.content || '*Nothing to preview yet*'}</ReactMarkdown>
                            </div>
                        )}
                    </div>
                </Field>

                <div className="flex gap-3 pt-2">
                    <button type="submit" disabled={saving} className="px-5 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 disabled:opacity-50 transition-colors">
                        {saving ? 'Saving...' : 'Save Changes'}
                    </button>
                    <Link href="/admin/lessons" className="px-5 py-2 rounded-lg border border-border text-sm hover:bg-muted transition-colors">
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
