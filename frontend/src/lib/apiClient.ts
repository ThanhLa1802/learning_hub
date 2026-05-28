import {
    AddMessageRequest,
    CompleteSessionRequest,
    CreateSessionRequest,
    Difficulty,
    PaginatedResponse,
    PracticeMode,
    PracticeSession,
    Scenario,
    ScenarioCategory,
    SessionMessage,
    User,
} from '@/types'
import { api } from './api'

// Auth
export const authApi = {
    register: (data: { email: string; password: string; full_name: string }) =>
        api.post<User>('/auth/register', data),
    login: (data: { email: string; password: string }) =>
        api.post<{ access_token: string }>('/auth/login', data),
    logout: () => api.post('/auth/logout'),
    refresh: () => api.post('/auth/refresh'),
}

// Users
export const usersApi = {
    me: () => api.get<User>('/users/me'),
}

// Scenarios
export const scenariosApi = {
    getCategories: () => api.get<ScenarioCategory[]>('/scenarios/categories'),
    getAll: (params?: { category_id?: string; difficulty?: Difficulty; mode?: PracticeMode }) =>
        api.get<Scenario[]>('/scenarios', { params }),
    getById: (id: string) => api.get<Scenario>(`/scenarios/${id}`),
}

// Sessions
export const sessionsApi = {
    create: (data: CreateSessionRequest) => api.post<PracticeSession>('/sessions', data),
    list: (skip = 0, limit = 10) =>
        api.get<PaginatedResponse<PracticeSession>>('/sessions', { params: { skip, limit } }),
    getById: (id: string) => api.get<PracticeSession>(`/sessions/${id}`),
    addMessage: (id: string, data: AddMessageRequest) =>
        api.post<SessionMessage[]>(`/sessions/${id}/messages`, data),
    complete: (id: string, data: CompleteSessionRequest) =>
        api.post<PracticeSession>(`/sessions/${id}/complete`, data),
}

// Admin
export interface AdminDomain {
    id: string; slug: string; name: string; description: string
    icon_name: string; color: string; order_index: number; is_active: boolean
}
export interface AdminCourse {
    id: string; domain_id: string; domain_name: string; slug: string
    name: string; description: string; order_index: number; is_active: boolean
}
export interface AdminLesson {
    id: string; course_id: string; course_name: string; domain_name: string
    title: string; content_type: string; order_index: number
    estimated_minutes: number; is_active: boolean
}
export interface AdminLessonPage {
    items: AdminLesson[]; total: number; page: number; pages: number
}
export interface AdminLessonDetail extends AdminLesson {
    content: string; category_id?: string
}

export const adminApi = {
    // Domains
    getDomains: () => api.get<AdminDomain[]>('/admin/domains'),
    createDomain: (data: Omit<AdminDomain, 'id'>) => api.post<AdminDomain>('/admin/domains', data),
    updateDomain: (id: string, data: Partial<AdminDomain>) => api.put<AdminDomain>(`/admin/domains/${id}`, data),

    // Courses
    getCourses: () => api.get<AdminCourse[]>('/admin/courses'),
    createCourse: (data: Omit<AdminCourse, 'id' | 'domain_name'>) => api.post<AdminCourse>('/admin/courses', data),
    updateCourse: (id: string, data: Partial<AdminCourse>) => api.put<AdminCourse>(`/admin/courses/${id}`, data),

    // Lessons
    getLessons: (courseId?: string, page = 1) => api.get<AdminLessonPage>('/admin/lessons', { params: { ...(courseId ? { course_id: courseId } : {}), page } }),
    getLessonDetail: (id: string) => api.get<AdminLessonDetail & { content: string }>(`/admin/lessons/${id}`),
    createLesson: (data: Omit<AdminLessonDetail, 'id' | 'course_name' | 'domain_name'>) => api.post<AdminLessonDetail>('/admin/lessons', data),
    updateLesson: (id: string, data: Partial<AdminLessonDetail>) => api.put<AdminLessonDetail>(`/admin/lessons/${id}`, data),
}
