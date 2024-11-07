import React, { createContext, useState, useContext, ReactNode } from 'react';

// Typ dla danych kontekstu użytkownika
interface UserContextType {
    userId: string | null;
    setUserId: (id: string | null) => void;
}

// Inicjalizujemy UserContext jako undefined lub z obiektem o zadanym typie
const UserContext = createContext<UserContextType | undefined>(undefined);

// Typy dla propsów UserProvider
interface UserProviderProps {
    children: ReactNode;
}

export const UserProvider: React.FC<UserProviderProps> = ({ children }) => {
    const [userId, setUserId] = useState<string | null>(null);

    return (
        <UserContext.Provider value={{ userId, setUserId }}>
            {children}
        </UserContext.Provider>
    );
};

// Hook, który zapewnia dostęp do UserContext z kontrolą typu
export const useUser = (): UserContextType => {
    const context = useContext(UserContext);
    if (context === undefined) {
        throw new Error('useUser must be used within a UserProvider');
    }
    return context;
};
