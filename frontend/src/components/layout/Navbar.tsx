'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { BookOpen, GraduationCap, History, LayoutDashboard, LogOut, ShieldAlert } from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { Button } from '@/components/ui/button'
import { ButtonLink } from '@/components/ui/button-link'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { toast } from 'sonner'
import { LanguageToggle } from '@/components/LanguageToggle'

export function Navbar() {
    const { user, logout } = useAuth()
    const router = useRouter()

    const handleLogout = async () => {
        await logout()
        toast.success('Logged out')
        router.push('/login')
    }

    const initials = user?.full_name
        .split(' ')
        .map((n) => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2)

    return (
        <header className="border-b border-border bg-card/50 backdrop-blur sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                <Link href="/dashboard" className="flex items-center gap-2.5 font-semibold text-xl">
                    <BookOpen className="h-6 w-6 text-primary" />
                    <span>DevEnglish</span>
                </Link>

                <nav className="hidden md:flex items-center gap-2">
                    <ButtonLink href="/dashboard" variant="ghost">
                        <LayoutDashboard className="h-5 w-5 mr-2" />
                        Dashboard
                    </ButtonLink>
                    <ButtonLink href="/learn" variant="ghost">
                        <GraduationCap className="h-5 w-5 mr-2" />
                        Learn
                    </ButtonLink>
                    <ButtonLink href="/history" variant="ghost">
                        <History className="h-5 w-5 mr-2" />
                        History
                    </ButtonLink>
                </nav>

                <div className="flex items-center gap-2">
                    <LanguageToggle />
                    {user && (
                        <DropdownMenu>
                            <DropdownMenuTrigger className="relative h-9 w-9 rounded-full inline-flex items-center justify-center hover:bg-muted transition-colors">
                                <Avatar className="h-8 w-8">
                                    <AvatarFallback className="text-xs bg-primary text-primary-foreground">{initials}</AvatarFallback>
                                </Avatar>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end" className="w-48">
                                <div className="px-2 py-1.5">
                                    <p className="text-sm font-medium">{user.full_name}</p>
                                    <p className="text-xs text-muted-foreground truncate">{user.email}</p>
                                </div>
                                <DropdownMenuSeparator />
                                <DropdownMenuItem onClick={() => router.push('/dashboard')} className="cursor-pointer">
                                    <LayoutDashboard className="h-4 w-4 mr-2" />
                                    Dashboard
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => router.push('/learn')} className="cursor-pointer">
                                    <GraduationCap className="h-4 w-4 mr-2" />
                                    Learn
                                </DropdownMenuItem>
                                <DropdownMenuItem onClick={() => router.push('/history')} className="cursor-pointer">
                                    <History className="h-4 w-4 mr-2" />
                                    History
                                </DropdownMenuItem>
                                {user.is_admin && (
                                    <DropdownMenuItem onClick={() => router.push('/admin')} className="cursor-pointer text-primary">
                                        <ShieldAlert className="h-4 w-4 mr-2" />
                                        Admin Panel
                                    </DropdownMenuItem>
                                )}
                                <DropdownMenuSeparator />
                                <DropdownMenuItem onClick={handleLogout} className="text-destructive cursor-pointer">
                                    <LogOut className="h-4 w-4 mr-2" />
                                    Log out
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                    )}
                </div>
            </div>
        </header>
    )
}
