import type { Store, _GettersTree } from 'pinia'

// Types pour les réactions
export type ReactionType = string | number;

export interface ReactionCount {
    [key: string | number]: number;
}

// Fonction utilitaire pour convertir une réaction en chaîne
export const reactionToString = (reaction: ReactionType): string => {
    return String(reaction);
}

// Types pour les communes
export interface Commune {
    id: number;
    nom: string;
    region: string;
    latitude: number | null;
    longitude: number | null;
    created_at: string;
    updated_at: string;
}

// État du store
export interface CommuneState {
    communes: Commune[];
    isLoading: boolean;
    error: string | null;
}

// Getters du store
export interface CommuneGetters extends _GettersTree<CommuneState> {
    getCommuneById: (state: CommuneState) => (id: number) => Commune | null;
    getCommuneOptions: (state: CommuneState) => { value: number; label: string }[];
    getCommunesWithCoordinates: (state: CommuneState) => Commune[];
    getRegions: (state: CommuneState) => string[];
}

// Actions du store
export interface CommuneActions {
    fetchCommunes: () => Promise<void>;
    searchCommunes: (searchTerm: string) => Promise<Commune[]>;
    getCommunesByRegion: (region: string) => Promise<Commune[]>;
    reset: () => void;
}

// Store complet
export interface CommuneStore extends Store<'commune', CommuneState, CommuneGetters, CommuneActions> {
    communes: Commune[];
    isLoading: boolean;
    error: string | null;
}

// Types pour les utilisateurs
export type UserRole = 'CITIZEN' | 'CTD' | 'ADMIN';

export interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    role: UserRole;
    commune?: Commune;
    created_at: string;
}

// Types pour les messages
export interface Message {
    id: number;
    temp_id?: string;  // ID temporaire pour les messages en attente
    content: string;
    author: User;
    created_at: string;
    is_edited: boolean;
    reply_to?: {
        id: number;
        content: string;
        author: string;
    };
    reactions_count: ReactionCount;
    user_reactions: ReactionType[];
    read_by: number[];
    isEditing?: boolean;
    editContent?: string;
    showReactions?: boolean;
}

export interface WebSocketMessage {
    type: 'message' | 'typing' | 'online' | 'read' | 'edit' | 'delete' | 'reaction' | 'message_ack';
    message?: Message;
    user?: User;
    is_typing?: boolean;
    users?: { user: User }[];
    message_id?: number;
    user_id?: number;
    temp_id?: string;  // ID temporaire pour les accusés de réception
}

// Types pour les projets
export interface Project {
    id: number;
    title: string;
    description: string;
    status: ProjectStatus;
    commune: Commune;
    start_date: string | null;
    end_date: string | null;
    budget: number | null;
    image: string | null;
    created_at: string;
    created_by: User;
    accountability_count: number;
}

export type ProjectStatus = 'PLANNED' | 'IN_PROGRESS' | 'COMPLETED' | 'SUSPENDED';

// Types pour les demandes de comptes
export interface Accountability {
    id: number;
    project: Project;
    citizen: User;
    question: string;
    response: string | null;
    status: AccountabilityStatus;
    created_at: string;
    updated_at: string;
    responded_by: User | null;
    responded_at: string | null;
}

export type AccountabilityStatus = 'PENDING' | 'ANSWERED' | 'CLOSED'; 