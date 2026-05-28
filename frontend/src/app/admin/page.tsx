'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Globe, BookOpen, FileText, PlusCircle } from 'lucide-react'
import { adminApi, AdminDomain, AdminCourse, AdminLesson } from '@/lib/apiClient'

export default function AdminDashboard() {
    const [domains, setDomains] = useState<AdminDomain[]>([])
    const [courses, setCourses] = useState<AdminCourse[]>([])
    const [lessons, setLessons] = useState<AdminLesson[]>([])

    useEffect(() => {
        adminApi.getDomains().then((r) => setDomains(r.data))
        adminApi.getCourses().then((r) => setCourses(r.data))
        adminApi.getLessons().then((r) => setLessons(r.data))
    }, [])

    const stats = [
        { label: 'Domains', value: domains.length, icon: Globe, href: '/admin/domains', color: 'text-blue-500' },
        { label: 'Courses', value: courses.length, icon: BookOpen, href: '/admin/courses', color: 'text-green-500' },
        { label: 'Lessons', value: lessons.length, icon: FileText, href: '/admin/lessons', color: 'text-purple-500' },
    ]

    return (
        <div>
            <h1 className="text-2xl font-bold mb-6">Overview</h1>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
                {stats.map(({ label, value, icon: Icon, href, color }) => (
                    <Link
                        key={href}
                        href={href}
                        className="rounded-xl border border-border bg-card p-5 hover:border-primary/40 transition-colors"
                    >
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-sm text-muted-foreground">{label}</span>
                            <Icon className={`h-5 w-5 ${color}`} />
                        </div>
                        <p className="text-3xl font-bold">{value}</p>
                    </Link>
                ))}
            </div>

            <h2 className="text-lg font-semibold mb-3">Quick Actions</h2>
            <div className="flex flex-wrap gap-3">
                <Link href="/admin/domains/new" className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors">
                    <PlusCircle className="h-4 w-4" /> New Domain
                </Link>
                <Link href="/admin/courses/new" className="flex items-center gap-2 px-4 py-2 rounded-lg bg-secondary text-secondary-foreground text-sm font-medium hover:bg-secondary/80 transition-colors">
                    <PlusCircle className="h-4 w-4" /> New Course
                </Link>
                <Link href="/admin/lessons/new" className="flex items-center gap-2 px-4 py-2 rounded-lg bg-secondary text-secondary-foreground text-sm font-medium hover:bg-secondary/80 transition-colors">
                    <PlusCircle className="h-4 w-4" /> New Lesson
                </Link>
            </div>
        </div>
    )
}
