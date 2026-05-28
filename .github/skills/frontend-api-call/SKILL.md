---
name: frontend-api-call
description: 'Add a new API call or service function to the frontend. Use when connecting a new page or component to the backend API, adding new fetch logic, creating new service functions, or wiring up new types for backend responses.'
argument-hint: 'Mô tả API call cần thêm (e.g. "fetch danh sách tags", "submit form tạo scenario")'
---

# Frontend API Call

## Nguyên tắc bắt buộc

- **LUÔN** dùng `api` instance từ `@/lib/api` — không tạo axios instance mới
- `api` đã có `withCredentials: true` và logic refresh token 401 tự động
- Không dùng `fetch()` ngoại trừ SSE streaming (practice chat)

## Pattern chuẩn

### 1. Định nghĩa Type — `frontend/src/types/`

Nếu liên quan đến **learning flow** → thêm vào `learn.ts`  
Nếu liên quan đến **practice flow** → thêm vào `index.ts`  
Tạo file mới chỉ khi resource hoàn toàn độc lập.

```typescript
// frontend/src/types/learn.ts
export interface Tag {
    id: string
    name: string
    slug: string
}
```

### 2. Thêm Service Function — `frontend/src/services/learnApi.ts`

```typescript
import { api } from '@/lib/api'
import { Tag } from '@/types/learn'

export const tagsApi = {
    getAll: (lang = 'en') =>
        api.get<Tag[]>('/tags', { params: { lang } }),

    getById: (id: string) =>
        api.get<Tag>(`/tags/${id}`),

    create: (data: { name: string }) =>
        api.post<Tag>('/tags', data),
}
```

### 3. Dùng trong Component / Page

```typescript
// Trong Server Component (Next.js App Router) — KHÔNG dùng
// Server components không thể gửi cookie → dùng Client Component

// Trong Client Component
'use client'
import { useEffect, useState } from 'react'
import { tagsApi } from '@/services/learnApi'
import { useLang } from '@/hooks/useLang'

export function TagList() {
    const { lang } = useLang()
    const [tags, setTags] = useState<Tag[]>([])

    useEffect(() => {
        tagsApi.getAll(lang)
            .then(res => setTags(res.data))
            .catch(console.error)
    }, [lang])

    return <ul>{tags.map(t => <li key={t.id}>{t.name}</li>)}</ul>
}
```

### 4. SSE Streaming (chỉ dùng cho practice chat)

Dùng native `fetch` với `credentials: 'include'` — **không** dùng axios:

```typescript
const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/sessions/${id}/messages/stream`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: message }),
})

const reader = res.body!.getReader()
const decoder = new TextDecoder()

while (true) {
    const { done, value } = await reader.read()
    if (done) break
    const chunk = decoder.decode(value)
    // parse "data: {...}\n\n" events
    // payload types: user_msg | token | done
}
```

## Bilingual (đa ngôn ngữ)

Lấy lang từ context, truyền vào API:

```typescript
import { useLang } from '@/hooks/useLang'

const { lang } = useLang()
domainsApi.getAll(lang)  // truyền lang vào mọi API hỗ trợ i18n
```

## Checklist

- [ ] Dùng `api` từ `@/lib/api`, không tạo axios mới
- [ ] Type định nghĩa trong đúng file (`learn.ts` hoặc `index.ts`)
- [ ] Service function nằm trong file service phù hợp (`learnApi.ts` hoặc mới)
- [ ] Component là `'use client'` nếu gọi API (cookie-based auth không work ở server)
- [ ] Truyền `lang` từ `useLang()` cho API hỗ trợ i18n
- [ ] SSE dùng native `fetch`, không dùng axios

## Tham khảo

- [api.ts](../../frontend/src/lib/api.ts) — Axios instance + refresh logic
- [learnApi.ts](../../frontend/src/services/learnApi.ts) — Service functions mẫu
- [learn.ts](../../frontend/src/types/learn.ts) — Types mẫu
- [LangContext.tsx](../../frontend/src/contexts/LangContext.tsx) — useLang hook
