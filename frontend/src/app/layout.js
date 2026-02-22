import {ClerkProvider} from '@clerk/nextjs'
import Header from "@/components/Header";
import {Geist, Geist_Mono} from 'next/font/google'
import './globals.css'

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
        <ClerkProvider>
            <html lang="en">
            <body
                className={`${geistSans.variable} ${geistMono.variable} antialiased`}
            >
            <Header/>
            {children}
            </body>
            </html>
        </ClerkProvider>
    )
}
