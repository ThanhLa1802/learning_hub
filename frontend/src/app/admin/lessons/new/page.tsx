'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft, Eye, Code } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { adminApi, AdminCourse } from '@/lib/apiClient'

const CONTENT_TYPES = ['explanation', 'practice', 'example', 'exercise', 'quiz']

export default function NewLessonPage() {
    const router = useRouter()
    const [courses, setCourses] = useState<AdminCourse[]>([])
    const [saving, setSaving] = useState(false)
    const [error, setError] = useState('')
    const [preview, setPreview] = useState(false)
    const [form, setForm] = useState({
        course_id: '', title: '', content: '',
        content_type: 'explanation', order_index: 0,
        estimated_minutes: 10, is_active: true,
    })

    useEffect(() => {
        adminApi.getCourses().then((r) => {
            setCourses(r.data)
            if (r.data.length > 0) setForm((f) => ({ ...f, course_id: r.data[0].id }))
        })
    }, [])

    const set = (k: keyof typeof form, v: unknown) => setForm((f) => ({ ...f, [k]: v }))

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault()
        setError('')
        setSaving(true)
        try {
            await adminApi.createLesson(form)
            router.push('/admin/lessons')
        } catch (err: unknown) {
            const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
            setError(msg ?? 'Failed to create lesson')
        } finally {
            setSaving(false)
        }
    }

    return (
        <div>
            <Link href="/admin/lessons" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-6">
                <ArrowLeft className="h-4 w-4" /> Lessons
            </Link>
            <h1 className="text-2xl font-bold mb-6">New Lesson</h1>

            {error && <p className="text-sm text-destructive bg-destructive/10 rounded-lg px-3 py-2 mb-4">{error}</p>}

            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                    <Field label="Course" required>
                        <select className="input" value={form.course_id} onChange={(e) => set('course_id', e.target.value)} required>
                            {courses.map((c) => <option key={c.id} value={c.id}>{c.domain_name} — {c.name}</option>)}
                        </select>
                    </Field>
                    <Field label="Content type">
                        <select className="input" value={form.content_type} onChange={(e) => set('content_type', e.target.value)}>
                            {CONTENT_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
                        </select>
                    </Field>
                </div>

                <Field label="Title" required>
                    <input className="input" value={form.title} onChange={(e) => set('title', e.target.value)} placeholder="Lesson title" required />
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
                                placeholder="Write lesson content in Markdown..."
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
                        {saving ? 'Saving...' : 'Create Lesson'}
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
