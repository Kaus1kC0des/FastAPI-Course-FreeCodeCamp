"use client";

import {Sidebar, SidebarContent, SidebarMenu, SidebarMenuItem, SidebarMenuButton} from "@/components/ui/sidebar";
import {Home, Bookmark, BookOpenText} from "lucide-react";

const SIDEBAR_KEYBOARD_SHORTCUT = "b";
const SIDEBAR_WIDTH = "16rem";
const SIDEBAR_WIDTH_MOBILE = "18rem";

export function AppSidebar() {
    return (
        <Sidebar variant="floating" collapsible="offcanvas">
            <SidebarContent>
                <div className="p-4">
                    <SidebarMenu className="flex flex-col gap-4">
                        <SidebarMenuItem>
                            <SidebarMenuButton asChild size="xl">
                                <a href="/home" className="text-xl">
                                    <Home className="!size-6" color="black"/>
                                    Home
                                </a>
                            </SidebarMenuButton>
                        </SidebarMenuItem>
                        <SidebarMenuItem>
                            <SidebarMenuButton asChild size="xl">
                                <a href="/new-story" className="text-xl">
                                    <Bookmark className="!size-6"/>
                                    Library
                                </a>
                            </SidebarMenuButton>
                        </SidebarMenuItem>
                        <SidebarMenuItem>
                            <SidebarMenuButton asChild size="xl">
                                <a href="/home" className="text-xl">
                                    <BookOpenText className="!size-6"/>
                                    Stories
                                </a>
                            </SidebarMenuButton>
                        </SidebarMenuItem>
                    </SidebarMenu>
                </div>
            </SidebarContent>
        </Sidebar>
    )
}