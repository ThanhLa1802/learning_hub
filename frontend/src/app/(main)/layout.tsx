'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { Navbar } from '@/components/layout/Navbar'
import { LangProvider } from '@/contexts/LangContext'

export default function MainLayout({ children }: { children: React.ReactNode }) {
    const { user, loading } = useAuth()
    const router = useRouter()

    useEffect(() => {
        if (!loading && !user) {
            router.push('/login')
        }
    }, [user, loading, router])

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="h-8 w-8 rounded-full border-2 border-primary border-t-transparent animate-spin" />
            </div>
        )
    }

    if (!user) return null

    return (
        <LangProvider>
            <div className="min-h-screen flex flex-col">
                <Navbar />
                <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-8">{children}</main>
            </div>
        </LangProvider>
    )
}
