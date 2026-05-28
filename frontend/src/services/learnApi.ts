import {
    AIExplainRequest,
    AIExplainResponse,
    DomainWithCourses,
    Lesson,
    LessonSummary,
    Quiz,
    QuizAttemptResult,
    UserProgress,
} from '@/types/learn'
import { api } from '@/lib/api'

export const domainsApi = {
    getAll: (lang = 'en') => api.get<DomainWithCourses[]>('/domains', { params: { lang } }),
    getBySlug: (slug: string, lang = 'en') => api.get<DomainWithCourses>(`/domains/${slug}`, { params: { lang } }),
    getLessons: (slug: string, categoryId?: string, lang = 'en') =>
        api.get<LessonSummary[]>(`/domains/${slug}/lessons`, {
            params: { lang, ...(categoryId ? { category_id: categoryId } : {}) },
        }),
}

export const lessonsApi = {
    getById: (id: string, lang = 'en') => api.get<Lesson>(`/lessons/${id}`, { params: { lang } }),
    explain: (id: string, data: AIExplainRequest, lang = 'en') =>
        api.post<AIExplainResponse>(`/lessons/${id}/explain`, data, { params: { lang } }),
    complete: (id: string) => api.post(`/lessons/${id}/complete`),
}

export const quizzesApi = {
    getById: (id: string, lang = 'en') => api.get<Quiz>(`/quizzes/${id}`, { params: { lang } }),
    submit: (id: string, answers: number[]) =>
        api.post<QuizAttemptResult>(`/quizzes/${id}/attempt`, { answers }),
}

export const progressApi = {
    getAll: () => api.get<UserProgress>('/progress'),
}
