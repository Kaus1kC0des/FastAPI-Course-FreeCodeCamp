import {ClerkProvider} from '@clerk/nextjs'
import Header from "@/components/Header";
import {Geist, Geist_Mono} from 'next/font/google'
import './globals.css'
import {SidebarProvider} from "@/components/ui/sidebar";
import { Providers } from './providers';
import {AppSidebar} from "@/components/SideBar";

const geistSans = Geist({
    variable: '--font-geist-sans',
    subsets: ['latin'],
})

const geistMono = Geist_Mono({
    variable: '--font-geist-mono',
    subsets: ['latin'],
})

export const metadata = [
    {title: 'Blog Application', description: 'Express your thoughts and share your ideas with the world!'},
    {}
]

export default function RootLayout({children}) {
    return (
        <html>
            <body
                className={`${geistSans.variable} ${geistMono.variable} antialiased`}
                >
                <Providers>
                    <ClerkProvider>
                        <SidebarProvider defaultOpen={false}>
                            <AppSidebar/>
                            <div className="flex flex-col flex-1">
                                <Header/>
                                <main className="flex-1">
                                    {children}
                                </main>
                            </div>
                        </SidebarProvider>
                    </ClerkProvider>
                </Providers>
            </body>
        </html>
    )
}
