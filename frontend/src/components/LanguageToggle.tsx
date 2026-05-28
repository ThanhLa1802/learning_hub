'use client'

import { useLang } from '@/contexts/LangContext'
import { Button } from '@/components/ui/button'

export function LanguageToggle() {
    const { lang, toggle } = useLang()

    return (
        <Button
            variant="outline"
            size="sm"
            onClick={toggle}
            className="font-mono text-xs h-8 px-2.5 min-w-[52px]"
            title={lang === 'en' ? 'Switch to Vietnamese' : 'Chuyển sang tiếng Anh'}
        >
            {lang === 'en' ? '🇺🇸 EN' : '🇻🇳 VI'}
        </Button>
    )
}
