'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { PlusCircle, Pencil, CheckCircle, XCircle } from 'lucide-react'
import { adminApi, AdminLesson, AdminCourse } from '@/lib/apiClient'

export default function LessonsPage() {
    const [lessons, setLessons] = useState<AdminLesson[]>([])
    const [courses, setCourses] = useState<AdminCourse[]>([])
    const [selectedCourse, setSelectedCourse] = useState('')
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        adminApi.getCourses().then((r) => setCourses(r.data))
    }, [])

    useEffect(() => {
        setLoading(true)
        adminApi.getLessons(selectedCourse || undefined)
            .then((r) => setLessons(r.data))
            .finally(() => setLoading(false))
    }, [selectedCourse])

    return (
        <div>
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-2xl font-bold">Lessons</h1>
                <Link
                    href="/admin/lessons/new"
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors"
                >
                    <PlusCircle className="h-4 w-4" /> New Lesson
                </Link>
            </div>

            <div className="mb-4">
                <select
                    className="input max-w-xs"
                    value={selectedCourse}
                    onChange={(e) => setSelectedCourse(e.target.value)}
                >
                    <option value="">All courses</option>
                    {courses.map((c) => <option key={c.id} value={c.id}>{c.domain_name} — {c.name}</option>)}
                </select>
            </div>

            {loading ? (
                <p className="text-muted-foreground text-sm">Loading...</p>
            ) : (
                <div className="border border-border rounded-xl overflow-hidden">
                    <table className="w-full text-sm">
                        <thead className="bg-muted text-muted-foreground">
                            <tr>
                                <th className="text-left px-4 py-3 font-medium">Title</th>
                                <th className="text-left px-4 py-3 font-medium">Course</th>
                                <th className="text-left px-4 py-3 font-medium">Domain</th>
                                <th className="text-left px-4 py-3 font-medium">Type</th>
                                <th className="text-left px-4 py-3 font-medium">Order</th>
                                <th className="text-left px-4 py-3 font-medium">Active</th>
                                <th className="px-4 py-3" />
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border">
                            {lessons.map((l) => (
                                <tr key={l.id} className="hover:bg-muted/40 transition-colors">
                                    <td className="px-4 py-3 font-medium max-w-[200px] truncate">{l.title}</td>
                                    <td className="px-4 py-3 text-muted-foreground text-xs">{l.course_name}</td>
                                    <td className="px-4 py-3 text-muted-foreground text-xs">{l.domain_name}</td>
                                    <td className="px-4 py-3 text-muted-foreground text-xs">{l.content_type}</td>
                                    <td className="px-4 py-3 text-muted-foreground">{l.order_index}</td>
                                    <td className="px-4 py-3">
                                        {l.is_active
                                            ? <CheckCircle className="h-4 w-4 text-green-500" />
                                            : <XCircle className="h-4 w-4 text-muted-foreground" />}
                                    </td>
                                    <td className="px-4 py-3 text-right">
                                        <Link
                                            href={`/admin/lessons/${l.id}`}
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
