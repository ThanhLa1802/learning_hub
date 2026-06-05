'use client'

import { useEffect, useState } from 'react'
import { useTheme } from 'next-themes'
import { Moon, Sun } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function ThemeToggle() {
    const { theme, setTheme } = useTheme()
    const [mounted, setMounted] = useState(false)

    // Prevent hydration mismatch — render only after client mount
    useEffect(() => { setMounted(true) }, [])
    if (!mounted) {
        return <Button variant="outline" size="sm" className="h-8 w-8 px-0" disabled aria-label="Theme toggle" />
    }

    const isDark = theme === 'dark'

    return (
        <Button
            variant="outline"
            size="sm"
            onClick={() => setTheme(isDark ? 'light' : 'dark')}
            className="h-8 w-8 px-0"
            title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
            aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
        >
            {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
        </Button>
    )
}
