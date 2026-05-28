'use client'

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import Link from 'next/link'
import { LayoutDashboard, Globe, BookOpen, FileText, ArrowLeft, ShieldAlert } from 'lucide-react'
import { usersApi } from '@/lib/apiClient'
import { User } from '@/types'

const NAV = [
    { href: '/admin', label: 'Overview', icon: LayoutDashboard, exact: true },
    { href: '/admin/domains', label: 'Domains', icon: Globe, exact: false },
    { href: '/admin/courses', label: 'Courses', icon: BookOpen, exact: false },
    { href: '/admin/lessons', label: 'Lessons', icon: FileText, exact: false },
]

export default function AdminLayout({ children }: { children: React.ReactNode }) {
    const router = useRouter()
    const pathname = usePathname()
    const [user, setUser] = useState<User | null>(null)
    const [checking, setChecking] = useState(true)

    useEffect(() => {
        usersApi.me()
            .then((r) => {
                if (!r.data.is_admin) {
                    router.replace('/')
                } else {
                    setUser(r.data)
                }
            })
            .catch(() => router.replace('/login'))
            .finally(() => setChecking(false))
    }, [router])

    if (checking) {
        return (
            <div className="flex h-screen items-center justify-center bg-background">
                <div className="h-8 w-8 rounded-full border-2 border-primary border-t-transparent animate-spin" />
            </div>
        )
    }

    if (!user) return null

    return (
        <div className="flex h-screen bg-background overflow-hidden">
            {/* Sidebar */}
            <aside className="w-56 border-r border-border flex flex-col shrink-0">
                <div className="px-4 py-5 border-b border-border">
                    <div className="flex items-center gap-2 text-primary font-bold text-base">
                        <ShieldAlert className="h-5 w-5" />
                        Admin Panel
                    </div>
                    <p className="text-xs text-muted-foreground mt-0.5 truncate">{user.email}</p>
                </div>

                <nav className="flex-1 p-3 space-y-1">
                    {NAV.map(({ href, label, icon: Icon, exact }) => {
                        const active = exact ? pathname === href : pathname.startsWith(href)
                        return (
                            <Link
                                key={href}
                                href={href}
                                className={`flex items-center gap-2.5 px-3 py-2 rounded-md text-sm transition-colors ${active
                                        ? 'bg-primary/10 text-primary font-medium'
                                        : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                                    }`}
                            >
                                <Icon className="h-4 w-4 shrink-0" />
                                {label}
                            </Link>
                        )
                    })}
                </nav>

                <div className="p-3 border-t border-border">
                    <Link
                        href="/learn"
                        className="flex items-center gap-2 px-3 py-2 rounded-md text-sm text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
                    >
                        <ArrowLeft className="h-4 w-4" />
                        Back to App
                    </Link>
                </div>
            </aside>

            {/* Main content */}
            <main className="flex-1 overflow-y-auto">
                <div className="max-w-6xl mx-auto p-6">
                    {children}
                </div>
            </main>
        </div>
    )
}
