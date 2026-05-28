'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { PlusCircle, Pencil, CheckCircle, XCircle } from 'lucide-react'
import { adminApi, AdminCourse } from '@/lib/apiClient'

export default function CoursesPage() {
    const [courses, setCourses] = useState<AdminCourse[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        adminApi.getCourses()
            .then((r) => setCourses(r.data))
            .finally(() => setLoading(false))
    }, [])

    return (
        <div>
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-2xl font-bold">Courses</h1>
                <Link
                    href="/admin/courses/new"
                    className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors"
                >
                    <PlusCircle className="h-4 w-4" /> New Course
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
                                <th className="text-left px-4 py-3 font-medium">Domain</th>
                                <th className="text-left px-4 py-3 font-medium">Slug</th>
                                <th className="text-left px-4 py-3 font-medium">Order</th>
                                <th className="text-left px-4 py-3 font-medium">Active</th>
                                <th className="px-4 py-3" />
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border">
                            {courses.map((c) => (
                                <tr key={c.id} className="hover:bg-muted/40 transition-colors">
                                    <td className="px-4 py-3 font-medium">{c.name}</td>
                                    <td className="px-4 py-3 text-muted-foreground">{c.domain_name}</td>
                                    <td className="px-4 py-3 text-muted-foreground font-mono text-xs">{c.slug}</td>
                                    <td className="px-4 py-3 text-muted-foreground">{c.order_index}</td>
                                    <td className="px-4 py-3">
                                        {c.is_active
                                            ? <CheckCircle className="h-4 w-4 text-green-500" />
                                            : <XCircle className="h-4 w-4 text-muted-foreground" />}
                                    </td>
                                    <td className="px-4 py-3 text-right">
                                        <Link
                                            href={`/admin/courses/${c.id}`}
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
